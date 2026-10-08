"""Portable storage paths and shared Proton process boundaries."""
import importlib.machinery
import importlib.util
import ast
import json
import os
from pathlib import Path
import tempfile
import struct
import subprocess
import shutil
import unittest
import socket
import threading
import ctypes
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.machinery.SourceFileLoader('uu_steamos', str(ROOT / 'scripts/uu-steamos'))
spec = importlib.util.spec_from_loader(loader.name, loader)
runtime = importlib.util.module_from_spec(spec)
loader.exec_module(runtime)
cursor_spec = importlib.util.spec_from_file_location('steamos_cursor', ROOT / 'scripts/uu-steamos-cursor.py')
cursor_module = importlib.util.module_from_spec(cursor_spec)
cursor_spec.loader.exec_module(cursor_module)
game_spec = importlib.util.spec_from_file_location('gamescope_input', ROOT / 'scripts/uu-gamescope-input.py')
game_module = importlib.util.module_from_spec(game_spec)
game_spec.loader.exec_module(game_module)
menus_spec = importlib.util.spec_from_file_location('steamos_menus', ROOT / 'scripts/uu-steamos-menus.py')
menus_module = importlib.util.module_from_spec(menus_spec)
menus_spec.loader.exec_module(menus_module)


class SteamOSMenuTests(unittest.TestCase):
    def test_ownerless_menu_uses_visible_fullscreen_viewer_from_same_process(self):
        menu = {'id': 3, 'pid': 20, 'uu': True, 'owner': None,
                'states': {'above', 'skip_taskbar', 'skip_pager'}}
        other = {'id': 1, 'pid': 30, 'uu': True, 'owner': None,
                 'states': {'fullscreen'}}
        viewer = {**other, 'id': 2, 'pid': 20}
        self.assertEqual(menus_module.menu_owner(menu, [other, viewer, menu]), 2)
        self.assertIsNone(menus_module.menu_owner(menu, [other, menu]))
        self.assertIsNone(menus_module.menu_owner(menu, [{**viewer, 'uu': False}, menu]))
        self.assertIsNone(menus_module.menu_owner(menu, [{**viewer, 'states': {'fullscreen', 'hidden'}}, menu]))

    def test_normal_windows_and_existing_tool_ownership_are_preserved(self):
        viewer = {'id': 2, 'pid': 20, 'uu': True, 'owner': None,
                  'states': {'fullscreen'}}
        menu = {**viewer, 'id': 3, 'states': {'above', 'skip_taskbar', 'skip_pager'}}
        self.assertIsNone(menus_module.menu_owner({**menu, 'owner': 4}, [viewer]))
        self.assertIsNone(menus_module.menu_owner({**menu, 'states': {'above'}}, [viewer]))


class SteamOSStorageTests(unittest.TestCase):
    def test_gamescope_uses_existing_session_sockets_and_root_local_gstreamer_cache(self):
        session = {'DISPLAY': ':0', 'WAYLAND_DISPLAY': 'gamescope-0',
                   'XDG_RUNTIME_DIR': '/run/user/2000', 'UURB_SESSION_KIND': 'gamescope'}
        with patch.object(runtime, 'session_environment', return_value=session):
            env = runtime.environment(Path('/portable/UU'), Path('/proton/proton'))
        self.assertEqual(env['UURB_SESSION_KIND'], 'gamescope')
        self.assertEqual(env['UURB_GAMESCOPE_EIS'], '/run/user/2000/gamescope-0-ei')
        self.assertEqual(env['GST_REGISTRY'], '/portable/UU/cache/gst-registry.bin')

    def test_gamescope_does_not_require_or_version_check_plasma_krdp(self):
        def available(command):
            return None if command in ('krdpserver', 'xfreerdp3') else '/usr/bin/' + command
        with patch.object(runtime.shutil, 'which', side_effect=available), \
                patch.object(runtime.subprocess, 'run') as execute:
            runtime.check_dependencies('gamescope')
            execute.assert_not_called()

    def test_discovers_latest_stable_proton_in_external_library(self):
        with tempfile.TemporaryDirectory() as directory:
            steam = Path(directory) / 'user/Steam'
            library = Path(directory) / 'external library'
            (steam / 'steamapps').mkdir(parents=True)
            (steam / 'steamapps/libraryfolders.vdf').write_text(
                '"libraryfolders" { "0" { "path" "' + str(library) + '" } }')
            for name in ('Proton 9.0', 'Proton 11.0', 'Proton Experimental'):
                proton = library / 'steamapps/common' / name
                (proton / 'files/bin').mkdir(parents=True)
                (proton / 'files/bin/wineserver').touch()
                (proton / 'proton').touch()
            self.assertEqual(runtime.discover_proton(steam),
                             (library / 'steamapps/common/Proton 11.0/proton').resolve())

    def test_root_is_inferred_from_portable_project_location(self):
        with patch.object(runtime, '__file__', '/portable disk/UURemote/project/scripts/uu-steamos'), \
                patch.dict(os.environ, {}, clear=True):
            self.assertEqual(runtime.default_root(), Path('/portable disk/UURemote'))

    def test_custom_steam_and_desktop_parameters_reach_runtime(self):
        desktop = {'DISPLAY': ':1', 'WAYLAND_DISPLAY': 'wayland-1',
                   'XDG_RUNTIME_DIR': '/run/user/2000'}
        with patch.object(runtime, 'session_environment', return_value=desktop):
            env = runtime.environment(Path('/portable/UU'), Path('/proton/proton'),
                                      Path('/custom/Steam'), {'monitor': 2, 'resolution': '1920x1080',
                                                             'rdp_port': 4400, 'private_display': 22})
        self.assertEqual(env['STEAM_COMPAT_CLIENT_INSTALL_PATH'], '/custom/Steam')
        self.assertEqual(env['UURB_MONITOR'], '2')
        self.assertEqual(env['UURB_RDP_PORT'], '4400')
        self.assertEqual(env['UURB_PRIVATE_DISPLAY'], '22')
        self.assertEqual(env['UURB_RESOLUTION'], '1920x1080')

    def test_generated_environment_keeps_large_artifacts_under_root(self):
        root = Path('/portable/UURemote')
        desktop = {'DISPLAY': ':0', 'XAUTHORITY': '/run/user/1000/auth',
                   'WAYLAND_DISPLAY': 'wayland-0', 'XDG_RUNTIME_DIR': '/run/user/1000'}
        with patch.object(runtime, 'session_environment', return_value=desktop):
            env = runtime.environment(root, root / 'tools/proton/proton')
        for name in ('HOME', 'XDG_CONFIG_HOME', 'XDG_CACHE_HOME', 'XDG_DATA_HOME',
                     'XDG_STATE_HOME', 'XDG_RUNTIME_DIR', 'TMPDIR', 'TMP', 'TEMP',
                     'STEAM_COMPAT_DATA_PATH', 'STEAM_COMPAT_SHADER_PATH',
                     'DXVK_STATE_CACHE_PATH', 'VKD3D_SHADER_CACHE_PATH',
                     'MESA_SHADER_CACHE_DIR', 'PROTON_LOG_DIR'):
            self.assertTrue(Path(env[name]).is_relative_to(root), name)
        self.assertEqual(env['WINEPREFIX'], '/portable/UURemote/compatdata/pfx')
        self.assertEqual(env['WAYLAND_DISPLAY'], '/run/user/1000/wayland-0')

    def test_proton_launcher_mirror_does_not_copy_runtime_payload(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'portable'
            (root / 'tools').mkdir(parents=True)
            installed = Path(directory) / 'steam/Proton 11.0'
            (installed / 'files/bin').mkdir(parents=True)
            (installed / 'files/bin/wineserver').touch()
            (installed / 'files/payload').write_bytes(b'original-runtime')
            for name in ('proton', 'filelock.py', 'version', 'proton_3.7_tracked_files'):
                (installed / name).write_text(name)
            mirror = runtime.prepare_proton(root, installed / 'proton')
            self.assertTrue(mirror.is_relative_to(root))
            self.assertTrue((mirror.parent / 'files').is_symlink())
            self.assertEqual((mirror.parent / 'files').resolve(), (installed / 'files').resolve())
            self.assertEqual((installed / 'files/payload').read_bytes(), b'original-runtime')
            self.assertFalse((installed / 'dist.lock').exists())

    def test_proton_metadata_symlink_cannot_write_into_steam(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'portable'
            (root / 'tools').mkdir(parents=True)
            installed = Path(directory) / 'steam'
            (installed / 'files/bin').mkdir(parents=True)
            (installed / 'files/bin/wineserver').touch()
            for name in ('proton', 'filelock.py', 'version', 'proton_3.7_tracked_files'):
                (installed / name).write_text(name)
            mirror = runtime.prepare_proton(root, installed / 'proton')
            mirror.unlink()
            mirror.symlink_to(installed / 'proton')
            with self.assertRaises(SystemExit):
                runtime.prepare_proton(root, installed / 'proton')
            self.assertEqual((installed / 'proton').read_text(), 'proton')


class SteamOSSandboxTests(unittest.TestCase):
    def test_nested_display_uses_private_bus_and_child_assigned_xwayland(self):
        from unittest.mock import Mock
        tree = ast.parse((ROOT / 'scripts/uu-steamos-session.py').read_text())
        function = next(item for item in tree.body if isinstance(item, ast.FunctionDef)
                        and item.name == 'prepare_manager_display')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'runtime').mkdir()
            host = Mock(pid=2345)
            host.poll.return_value = None
            calls = []

            def spawn(name, command, selected):
                calls.append((name, command, selected))
                if name == 'manager-dbus':
                    (root / 'runtime/manager-bus').touch()
                if name == 'manager-kwin':
                    (root / 'runtime/manager-display.json').write_text(
                        json.dumps({'DISPLAY': ':43', 'XAUTHORITY': ''}))
                return host

            def wait_until(predicate, description):
                self.assertTrue(predicate(), description)

            physical = {'DISPLAY': ':7', 'WAYLAND_DISPLAY': '/host/wayland-0',
                        'DBUS_SESSION_BUS_ADDRESS': 'unix:path=/host/bus',
                        'WINEDLLOVERRIDES': ''}
            namespace = {'root': root, 'manager_host': None, 'manager_env': {},
                         'physical_env': physical, 'private_display': ':30',
                         'Path': Path, 'os': os, 'json': json, 'spawn': spawn,
                         '__file__': str(ROOT / 'scripts/uu-steamos-session.py'),
                         'wait_until': wait_until, 'manager_surface': lambda: None,
                         'subprocess': Mock(run=Mock(return_value=Mock(returncode=0)))}
            exec(compile(ast.Module(body=[function], type_ignores=[]), 'display', 'exec'), namespace)
            namespace['prepare_manager_display']()
            self.assertEqual(namespace['manager_env']['DISPLAY'], ':43')
            self.assertEqual(namespace['manager_host_env']['DISPLAY'], ':7')
            physical['DISPLAY'] = ':8'
            self.assertEqual(namespace['manager_host_env']['DISPLAY'], ':7')
            self.assertEqual(namespace['manager_env']['DBUS_SESSION_BUS_ADDRESS'],
                             'unix:path=' + str(root / 'runtime/manager-bus'))
            self.assertNotIn('WAYLAND_DISPLAY', namespace['manager_env'])
            self.assertEqual(calls[1][1][1:3], ['--x11-display', ':7'])
            self.assertEqual(physical['DBUS_SESSION_BUS_ADDRESS'], 'unix:path=/host/bus')
            namespace['prepare_manager_display']()
            self.assertEqual(len(calls), 2)

    def test_closed_manager_hides_gamescope_surface_but_keeps_backend(self):
        from unittest.mock import Mock
        tree = ast.parse((ROOT / 'scripts/uu-steamos-session.py').read_text())
        function = next(item for item in tree.body if isinstance(item, ast.FunctionDef)
                        and item.name == 'manager_visible')
        execute = Mock()
        lookup = Mock(return_value=None)
        namespace = {'manager_running': lambda: True, 'find_manager': lookup,
                     'manager_surface': lambda: '12345', 'run': execute,
                     'manager_host_env': {'DISPLAY': ':0'},
                     'physical_env': {'UURB_SESSION_KIND': 'gamescope', 'DISPLAY': ':1'}}
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'manager_visible', 'exec'), namespace)
        self.assertFalse(namespace['manager_visible']())
        execute.assert_called_once_with(['xdotool', 'windowunmap', '12345'], namespace['manager_host_env'])
        lookup.return_value = '9876'
        execute.reset_mock()
        self.assertTrue(namespace['manager_visible']())
        execute.assert_not_called()

    def test_gamescope_surface_search_keeps_original_host_display_on_steam_reopen(self):
        from unittest.mock import Mock
        tree = ast.parse((ROOT / 'scripts/uu-steamos-session.py').read_text())
        function = next(item for item in tree.body if isinstance(item, ast.FunctionDef)
                        and item.name == 'manager_surface')
        host = Mock()
        host.pid = 2345
        host.poll.return_value = None
        execute = Mock(return_value=Mock(stdout=b'12345\n'))
        namespace = {'manager_host': host, 'manager_env': {'DISPLAY': ':23'},
                     'manager_host_env': {'DISPLAY': ':0'},
                     'physical_env': {'DISPLAY': ':1'}, 'subprocess': Mock(run=execute)}
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'manager_surface', 'exec'), namespace)
        self.assertEqual(namespace['manager_surface'](), '12345')
        self.assertEqual(execute.call_args.args[0],
                         ['xdotool', 'search', '--pid', '2345'])
        self.assertEqual(execute.call_args.kwargs['env']['DISPLAY'], ':0')
        host.poll.return_value = 1
        execute.reset_mock()
        self.assertIsNone(namespace['manager_surface']())
        execute.assert_not_called()

    def test_manager_lookup_does_not_mistake_host_container_for_uu_client(self):
        from unittest.mock import Mock
        tree = ast.parse((ROOT / 'scripts/uu-steamos-session.py').read_text())
        function = next(item for item in tree.body if isinstance(item, ast.FunctionDef)
                        and item.name == 'find_manager')
        execute = Mock(side_effect=[Mock(stdout=b'9876\n'),
                                   Mock(stdout=b'WIDTH=920\nHEIGHT=680\n')])
        namespace = {'manager_env': {'DISPLAY': ':23'}, 'subprocess': Mock(run=execute)}
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'find_manager', 'exec'), namespace)
        self.assertEqual(namespace['find_manager'](visible=True), '9876')
        for call in execute.call_args_list:
            self.assertEqual(call.kwargs['env']['DISPLAY'], ':23')

    def test_retained_wine_desktop_does_not_count_as_a_running_manager(self):
        tree = ast.parse((ROOT / 'scripts/uu-steamos-session.py').read_text())
        function = next(item for item in tree.body if isinstance(item, ast.FunctionDef)
                        and item.name == 'manager_running')
        with tempfile.TemporaryDirectory() as directory:
            processes = Path(directory)
            desktop = processes / '1'
            desktop.mkdir()
            (desktop / 'comm').write_text('explorer.exe\n')
            (desktop / 'environ').write_text('WINEPREFIX=/portable/pfx\0')
            (desktop / 'maps').write_text('1000-2000 r--p 0 0:0 1 /windows/explorer.exe\n')
            namespace = {'os': os, 'prefix': Path('/portable/pfx'),
                         'app': Path('/portable/pfx/drive_c/UU'),
                         'Path': lambda value: processes if value == '/proc' else Path(value)}
            exec(compile(ast.Module(body=[function], type_ignores=[]), 'manager_running', 'exec'), namespace)
            self.assertFalse(namespace['manager_running']())
            manager = processes / '2'
            manager.mkdir()
            (manager / 'comm').write_text('source=explorer\n')
            (manager / 'maps').write_text('1000-2000 r--p 0 0:0 1 /portable/pfx/drive_c/UU/bin/GameViewer.exe\n')
            (manager / 'environ').write_text('WINEPREFIX=/another/pfx\0')
            self.assertFalse(namespace['manager_running']())
            (manager / 'environ').write_text('WINEPREFIX=/portable/pfx\0')
            self.assertTrue(namespace['manager_running']())
            (manager / 'environ').write_text('WINEPREFIX=/portable/pfx/\0')
            self.assertTrue(namespace['manager_running']())

    def test_disconnected_control_client_cannot_kill_the_relay(self):
        tree = ast.parse((ROOT / 'scripts/uu-steamos-session.py').read_text())
        function = next(item for item in tree.body if isinstance(item, ast.FunctionDef)
                        and item.name == 'send_reply')
        namespace = {}
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'send_reply', 'exec'), namespace)
        disconnected, peer = socket.socketpair()
        peer.close()
        with disconnected:
            self.assertFalse(namespace['send_reply'](disconnected, b'ping'))
        left, right = socket.socketpair()
        with left, right:
            self.assertTrue(namespace['send_reply'](left, b'ready'))
            self.assertEqual(right.recv(32), b'ready')

    def test_stale_socket_is_not_a_running_session(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'runtime').mkdir()
            with socket.socket(socket.AF_UNIX) as server:
                server.bind(str(root / 'runtime/control.sock'))
            self.assertFalse(runtime.session_alive(root))

    def test_running_session_requires_a_successful_ping(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'runtime').mkdir()
            with socket.socket(socket.AF_UNIX) as server:
                server.bind(str(root / 'runtime/control.sock'))
                server.listen(1)
                def respond():
                    connection, _ = server.accept()
                    with connection:
                        self.assertEqual(connection.recv(32), b'ping')
                        connection.sendall(b'Portable session is running.\n')
                thread = threading.Thread(target=respond)
                thread.start()
                self.assertTrue(runtime.session_alive(root))
                thread.join(timeout=2)
                self.assertFalse(thread.is_alive())

    def test_wine_tools_share_pids_and_only_root_is_writable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'tmp').mkdir()
            with patch.object(runtime.subprocess, 'run') as execute:
                execute.return_value.returncode = 0
                runtime.sandbox(root, ['/bin/true'], {'DISPLAY': ':999'})
            args = execute.call_args.args[0]
            self.assertNotIn('--unshare-pid', args)
            self.assertNotIn('--unshare-ipc', args)
            self.assertIn('--ro-bind', args)
            self.assertIn(str(root / 'tmp'), args)
            self.assertIn(str(root / 'shm'), args)

    def test_steam_input_hotplug_directory_is_visible_to_proton(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'tmp').mkdir()
            exists = Path.exists
            with patch.object(Path, 'exists', lambda path: path == Path('/dev/input') or exists(path)), \
                    patch.object(runtime.subprocess, 'run') as execute:
                execute.return_value.returncode = 0
                runtime.sandbox(root, ['/bin/true'], {'DISPLAY': ':999'})
            args = execute.call_args.args[0]
            index = args.index('/dev/input')
            self.assertEqual(args[index - 1:index + 2], ['--dev-bind', '/dev/input', '/dev/input'])
            self.assertNotIn('/dev/uinput', args)


class GamescopeCoordinatesTests(unittest.TestCase):
    def test_centered_manager_and_letterboxed_game_use_surface_coordinates(self):
        for actual, expected in zip(game_module.map_position(640, 400, (1280, 800), (920, 680)), (460, 340)):
            self.assertAlmostEqual(actual, expected)
        for actual, expected in zip(game_module.map_position(640, 40, (1280, 800), (1920, 1080)), (960, 0)):
            self.assertAlmostEqual(actual, expected)
        self.assertEqual(game_module.map_position(0, 0, (1280, 800), (920, 680)), (0, 0))
        self.assertEqual(game_module.map_position(1280, 800, (1280, 800), (920, 680)), (919, 679))


class NativeCursorTests(unittest.TestCase):
    def test_gamescope_hidden_cursor_and_stale_hotspot_are_valid_cur_images(self):
        image = cursor_module.CursorImage()
        hidden = cursor_module.encode_native_cursor(image)
        self.assertEqual(struct.unpack_from('<BBBBHH', hidden, 6), (1, 1, 0, 0, 0, 0))
        image.width = image.height = 1
        image.xhot, image.yhot = 5, 3
        image.pixels = (ctypes.c_ulong * 1)(0)
        self.assertEqual(cursor_module.encode_native_cursor(image), hidden)
        image.width = 512
        self.assertIsNone(cursor_module.encode_native_cursor(image))

    def test_cur_preserves_size_hotspot_alpha_and_bottom_up_pixels(self):
        pixels = [0xff112233, 0x00123456, 0x80445566, 0xff778899]
        data = cursor_module.encode_cursor(2, 2, 1, 0, pixels)
        self.assertEqual(struct.unpack_from('<HHH', data), (0, 2, 1))
        self.assertEqual(struct.unpack_from('<BBBBHHII', data, 6),
                         (2, 2, 0, 0, 1, 0, 64, 22))
        self.assertEqual(struct.unpack_from('<ii', data, 26), (2, 4))
        self.assertEqual(struct.unpack_from('<4I', data, 62),
                         (pixels[2], pixels[3], pixels[0], pixels[1]))
        self.assertEqual(data[78:], b'\x00\x00\x00\x00\x40\x00\x00\x00')

    def test_invalid_dimensions_or_hotspot_are_rejected(self):
        for arguments in [(129, 1, 0, 0, []), (1, 1, 1, 0, [0]),
                          (1, 1, 0, 0, []), (0, 1, 0, 0, [])]:
            with self.assertRaises(ValueError):
                cursor_module.encode_cursor(*arguments)

    def test_proton_loads_native_shapes_and_retains_recent_handles(self):
        compiler = os.environ.get('UURB_TEST_MINGW_CC')
        proton = os.environ.get('UURB_PROTON')
        if not compiler or not proton:
            self.skipTest('Set UURB_TEST_MINGW_CC inside the Deck runtime for the Proton probe')
        source = r'''
#ifdef UNICODE
#undef UNICODE
#endif
#include "uu_cursor_guard.c"
#include <assert.h>
static BOOL WINAPI fake_info(PCURSORINFO info) {
    info->flags = 0; info->hCursor = NULL;
    info->ptScreenPos.x = 123; info->ptScreenPos.y = 234; return TRUE;
}
int wmain(int argc, wchar_t **argv) {
    assert(argc == 3); wcscpy(native_cursor_path, argv[1]);
    original_get_cursor_info = fake_info;
    CURSORINFO cursor = { .cbSize = sizeof(cursor) };
    ICONINFO icon; BITMAP bitmap;
    assert(guarded_get_cursor_info(&cursor)); assert(cursor.flags == CURSOR_SHOWING);
    assert(cursor.ptScreenPos.x == 123 && cursor.ptScreenPos.y == 234);
    assert(GetIconInfo(cursor.hCursor, &icon));
    assert(icon.xHotspot == 1 && icon.yHotspot == 0);
    assert(GetObjectW(icon.hbmColor, sizeof(bitmap), &bitmap));
    assert(bitmap.bmWidth == 2 && bitmap.bmHeight == 2);
    DeleteObject(icon.hbmColor); DeleteObject(icon.hbmMask);
    HCURSOR old = cursor.hCursor;
    assert(CopyFileW(argv[2], argv[1], FALSE)); Sleep(60);
    assert(guarded_get_cursor_info(&cursor)); assert(cursor.hCursor != old);
    assert(GetIconInfo(cursor.hCursor, &icon));
    assert(icon.xHotspot == 0 && icon.yHotspot == 0);
    assert(GetObjectW(icon.hbmColor, sizeof(bitmap), &bitmap));
    assert(bitmap.bmWidth == 3 && bitmap.bmHeight == 1);
    DeleteObject(icon.hbmColor); DeleteObject(icon.hbmMask);
    assert(GetIconInfo(old, &icon));
    DeleteObject(icon.hbmColor); DeleteObject(icon.hbmMask);
    puts("Native cursor dimensions, hotspots, updates and retained handles verified");
    return 0;
}
'''
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            file = folder / 'probe.c'
            file.write_text(source)
            first, second = folder / 'first.cur', folder / 'second.cur'
            first.write_bytes(cursor_module.encode_cursor(2, 2, 1, 0, [0xff112233] * 4))
            second.write_bytes(cursor_module.encode_cursor(3, 1, 0, 0, [0xff778899] * 3))
            executable = folder / 'probe.exe'
            subprocess.run([compiler, '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror',
                            '-municode', '-I', str(ROOT / 'src'), str(file),
                            '-o', str(executable), '-luser32', '-lgdi32'], check=True)
            windows_paths = ['Z:' + str(path).replace('/', '\\') for path in (first, second)]
            subprocess.run([proton, 'runinprefix', str(executable), *windows_paths],
                           check=True, timeout=30)


class PlasmaProtocolTests(unittest.TestCase):
    def test_authentication_and_fixed_point_coordinates_only_affect_fake_input(self):
        compiler = os.environ.get('UURB_TEST_CC', shutil.which('cc'))
        if not compiler:
            self.skipTest('Native C compiler unavailable')
        source = r'''
#define dlsym mock_dlsym
#include "uu_krdp_input_auth.c"
#include <assert.h>
#include <stdarg.h>
struct wl_proxy { const char *name; };
static struct wl_proxy fake = { "org_kde_kwin_fake_input" };
static struct wl_proxy seat = { "wl_seat" };
static unsigned int authentications, forwards;
static const char *class_name(struct wl_proxy *proxy) { return proxy->name; }
static uint32_t version(struct wl_proxy *proxy) { (void)proxy; return 4; }
static struct wl_proxy *forward(struct wl_proxy *proxy, uint32_t opcode,
    const struct wl_interface *interface, uint32_t version_number, uint32_t flags,
    union wl_argument *arguments) {
    (void)opcode; (void)version_number; (void)flags; (void)arguments;
    ++forwards; return interface ? proxy : NULL;
}
static struct wl_proxy *auth(struct wl_proxy *proxy, uint32_t opcode,
    const struct wl_interface *interface, uint32_t version_number, uint32_t flags, ...) {
    assert(proxy == &fake && opcode == 0 && !interface && version_number == 4 && flags == 0);
    va_list args; va_start(args, flags);
    assert(strcmp(va_arg(args, const char *), "UU SteamOS Desktop Relay") == 0);
    assert(strcmp(va_arg(args, const char *), "Remote desktop input") == 0);
    va_end(args); ++authentications; return NULL;
}
void *mock_dlsym(void *handle, const char *name) {
    (void)handle; void *symbol = NULL;
    if (!strcmp(name, "wl_proxy_marshal_array_flags")) {
        __typeof__(&forward) function = forward; memcpy(&symbol, &function, sizeof(symbol));
    } else if (!strcmp(name, "wl_proxy_marshal_flags")) {
        __typeof__(&auth) function = auth; memcpy(&symbol, &function, sizeof(symbol));
    } else if (!strcmp(name, "wl_proxy_get_class")) {
        __typeof__(&class_name) function = class_name; memcpy(&symbol, &function, sizeof(symbol));
    } else if (!strcmp(name, "wl_proxy_get_version")) {
        __typeof__(&version) function = version; memcpy(&symbol, &function, sizeof(symbol));
    }
    return symbol;
}
int main(void) {
    const struct wl_interface *interface = (const struct wl_interface *)&fake;
    assert(wl_proxy_marshal_array_flags(&fake, 0, interface, 4, 0, NULL) == &fake);
    assert(authentications == 1);
    assert(wl_proxy_marshal_array_flags(&seat, 0, interface, 4, 0, NULL) == &seat);
    assert(authentications == 1);
    union wl_argument coordinates[2] = {{.i = 500}, {.i = 600}};
    wl_proxy_marshal_array_flags(&fake, 9, NULL, 4, 0, coordinates);
    assert(coordinates[0].i == 128000 && coordinates[1].i == 153600);
    coordinates[0].i = 500; coordinates[1].i = 600;
    wl_proxy_marshal_array_flags(&seat, 9, NULL, 4, 0, coordinates);
    assert(coordinates[0].i == 500 && coordinates[1].i == 600);
    coordinates[0].i = INT32_MAX; coordinates[1].i = INT32_MIN;
    wl_proxy_marshal_array_flags(&fake, 9, NULL, 4, 0, coordinates);
    assert(coordinates[0].i == INT32_MAX && coordinates[1].i == INT32_MIN);
    union wl_argument wheel[2] = {{.u = 0}, {.i = 1}};
    wl_proxy_marshal_array_flags(&fake, 3, NULL, 4, 0, wheel);
    assert(wheel[0].u == 0 && wheel[1].i == 3840);
    wheel[0].u = 1; wheel[1].i = -2;
    wl_proxy_marshal_array_flags(&fake, 3, NULL, 4, 0, wheel);
    assert(wheel[0].u == 1 && wheel[1].i == -7680);
    wheel[1].i = 1;
    wl_proxy_marshal_array_flags(&seat, 3, NULL, 4, 0, wheel);
    assert(wheel[1].i == 1);
    assert(forwards == 8 && authentications == 1); return 0;
}
'''
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / 'protocol.c'
            file.write_text(source)
            executable = Path(directory) / 'protocol'
            subprocess.run([compiler, '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror',
                            '-I', str(ROOT / 'src'), str(file), '-o', str(executable),
                            '-ldl', '-pthread'], check=True)
            subprocess.run([str(executable)], check=True, timeout=10)


if __name__ == '__main__':
    unittest.main()
