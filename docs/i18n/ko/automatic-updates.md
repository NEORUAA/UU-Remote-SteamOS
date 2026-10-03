[English](../../automatic-updates.md) · [العربية](../ar/automatic-updates.md) · [Deutsch](../de/automatic-updates.md) · [Español](../es/automatic-updates.md) · [Français](../fr/automatic-updates.md) · [日本語](../ja/automatic-updates.md) · [한국어](../ko/automatic-updates.md) · [Русский](../ru/automatic-updates.md) · [Tiếng Việt](../vi/automatic-updates.md) · [简体中文](../zh-Hans/automatic-updates.md) · [繁體中文](../zh-Hant/automatic-updates.md)

[한국어 홈으로 돌아가기](../../../i18n/README.ko.md)

# 자동 확인과 재개 가능한 복구

유지관리 시스템은 릴레이를 끊지 않는 upstream 확인, 개인 소스 복구, 명시적 적용을 나눕니다. 정상 검사는 동작 중인 데스크톱을 교체하지 않습니다.

## 활성화

```bash
git switch main
git fetch --tags origin
./scripts/configure-updater.sh enable \
  --track v0.1.0 --branch main \
  --model codex-auto-review \
  --reasoning-effort medium \
  --auto-promote-accepted
```

Plus의 독립 릴리스 이력은 `v0.1.0`부터 시작합니다. 날짜가 붙은 입력 트랙 태그는 원본 프로젝트의 이력이며 이 독립 저장소에는 포함되지 않습니다. 일반 설치에는 필요하지 않습니다. Plus 태그가 로컬에 존재하면 `--track v0.1.0 --branch main`으로 명시적으로 선택합니다. 설정 도구의 기본값은 여전히 기존 트랙 이름이므로 없는 태그는 거부됩니다.

릴리스 태그를 체크아웃한 뒤 소스를 가져오는 일반 업그레이드를 실행하기 전에 `git switch main`을 실행합니다. 유지관리 브랜치는 `origin/main`이며 명시적 재설치 태그는 `v0.1.0`입니다. 업그레이드 중에도 고정 태그의 소스를 유지하려면 `--no-pull`을 사용합니다.

--auto-promote-accepted는 완전한 maintainer acceptance가 있는 정확한 버전에만 적용하며 Codex 자신의 draft를 배포하지 않습니다. 없으면 준비 상태만 보고합니다.

model/reasoning은 ~/.config/uu-remote-bridge/updater.json에 명시 저장합니다. 같은 사용자로 Codex 로그인해야 합니다. command -v codex 절대 경로를 저장해 NVM/systemd PATH 차이를 처리하며 --codex /absolute/path/to/codex로 선택합니다. 복구 전 포함 사용량을 조회하고 모든 window가 codex_max_used_percent(기본 20) 이하일 때 실행합니다. 구매/reset credits를 쓰지 않고 확인 불가 시 최소 한 시간 연기합니다.

## 타이머

| timer | 시점 | 작업 |
| --- | --- | --- |
| uu-remote-update-check.timer | 매일 04:20 전후＋임의 지연, 부팅 12분 뒤 | endpoint와 metadata |
| uu-remote-repair-monitor.timer | 부팅 7분 뒤, 완료 후 15분마다 | 상태, task 재개, 명시적 적용 |

Persistent=true인 daily는 꺼진 동안 놓친 한 번을 다음 부팅에 수행합니다. 대화형 터미널이 필요하지 않습니다.

```bash
uu-remote update
systemctl --user list-timers --all \
  uu-remote-update-check.timer uu-remote-repair-monitor.timer
journalctl --user -u uu-remote-update-check.service -n 100 --no-pager
journalctl --user -u uu-remote-repair-monitor.service -n 100 --no-pager
```

## 확인과 복구

일반 검사는 공식 redirect를 HEAD로 조회하고 임시 query key를 제거해 전체 버전을 비교합니다. 같은 버전은 SHA를 한 번 확정하고 ETag/size/sidecar를 재사용하며 오래된 endpoint는 업데이트로 취급하지 않습니다. monitor는 20초 간격 두 번의 이상을 기록하고 분석을 대기열에 넣으며 기본적으로 Wine/RDP/UU를 중지하지 않습니다.

--auto-reinstall은 별도 선택으로 확인된 고장에 한 번 restart, 이후 알려진 track을 build/test해 재설치합니다. 여기 활성화 예에는 켜지 않습니다. 새 파일은 downloads에 최대 1 GiB, 정적 추출 뒤 tasks 개인 clone에서 draft/test를 작성합니다. [유지관리 계약(English)](../../automated-repair-agent-handoff.md)을 0600 context로 보관합니다. 추출 불가 wrapper는 자동 실행하지 않고 명시적 --sandbox-install의 무네트워크 Bubblewrap/systemd를 씁니다. Codex는 live prefix, sudo, push나 자기 binary 승인을 하지 않습니다. [upstream 유지관리(English)](../../upstream-maintenance.md)를 따라 독립 확인합니다.

## 수용된 버전과 로그인 유지

공식 version/installer hash가 fetched origin/main의 approved manifest와 맞고, 같은 commit의 schema-1 acceptance와 evidence가 installer/server hash에 결합돼야 합니다. disposable prefix, 컨트롤러, 재연결, 냉기동, service restart, 새 signaling, 로그인 보존을 기록하며 안정 시간은 270–1800초입니다. 자동 적용을 명시 선택하고 활동이 조용한 기본 45분을 기다립니다.

runtime/account marker와 XRDP 상태를 확인하고 UU만 멈춘 뒤 전체 prefix를 복사하며 추가 1 GiB 공간을 확보합니다. 같은 prefix에 설치하고 정확한 patch를 적용하며 시작 전 registry/계정 트리를 byte 비교합니다. 초기 driver 처리와 새 room을 기다리고 안정 시간 사이의 두 검사를 거쳐 확정합니다. 실패·중단·재부팅은 이전 prefix를 복구해 promotion-blocked로 두고 자동 재시도를 멈춥니다. state/prefix는 같은 filesystem이며 snapshot은 보존합니다. XRDP 시작/중지/재시작은 하지 않습니다.

활동 대기만 건너뛰려면 다음을 사용합니다.

```bash
uu-remote upgrade apply --now
```

[재사용 업그레이드](reusable-upgrade.md)를 참고하세요.

## task 재개와 상태

0600 atomic task에 후보, track, base commit, context, thread UUID, attempt, phase, JSONL과 결과를 저장합니다. thread.started 때 UUID를 남기며 다음에 codex exec resume으로 같은 thread를 재개합니다. UUID가 없으면 같은 context로 새로 시작합니다. 간격은 15분에서 최대 24시간까지 늘어납니다. [결과 schema](../../../scripts/codex-repair-result.schema.json)를 따르고 monitor가 전체 unit suite를 별도로 실행합니다.

| 상태 | 뜻 |
| --- | --- |
| ready-for-review | 소스/검사 준비, 의미 검토와 실제 수용 대기 |
| no-change | 변경 없음 |
| blocked | 근거·staging·test·사람 판단 대기 |
| promotion-waiting-idle | 유휴 대기 |
| promotion-running | prefix 트랜잭션 진행 |
| promoted | 로그인/runtime 확인 |
| promotion-blocked | 이전 prefix 복구, 자동 재시도 중지 |

설정은 비밀번호/token이 없고 dir 0700/file 0600입니다. 개인 자료는 Git 밖에 둡니다. clone push URL을 끄고 Codex는 workspace-write/never, service는 NoNewPrivileges=yes입니다. 인증에 네트워크가 필요하며 VM 수준 격리는 아닙니다.

## Ubuntu 24.04 sandbox

PrivateTmp/ProtectSystem/ProtectKernelTunables/ProtectControlGroups namespace를 겹치면 AppArmor unprivileged_userns가 중첩 bwrap을 막으므로 사용자 서비스에서 쓰지 않습니다. codex-sandbox-deferred이면 배포판 bwrap profile만 설정합니다.

```bash
sudo apt install apparmor-profiles
sudo install -o root -g root -m 0644 \
  /usr/share/apparmor/extra-profiles/bwrap-userns-restrict \
  /etc/apparmor.d/bwrap-userns-restrict
sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict
uu-remote update retry
```

두 계층을 확인합니다.

```bash
systemd-run --user --wait --pipe --collect \
  --property=NoNewPrivileges=yes \
  /usr/bin/bwrap --die-with-parent --unshare-user --uid 0 --gid 0 \
  --ro-bind / / /bin/true
systemctl --user cat uu-remote-repair-monitor.service
```

probe가 성공하고 unit에 앞서 언급한 mount namespace가 없어야 합니다. retry는 근거/checkout을 유지하고 불가한 thread를 지워 다음에 새로 시작합니다. 지원하지 않는 phase는 거절합니다. 수동 fallback은 installer/server/healthd와 backend 기록 일치 후에 들여옵니다. ready-for-review에서 바로 배포하지 않습니다.

## 다른 기계와 비활성화

[입력 트랙(English)](../../release-tracks.md), clean tree, 같은 사용자 codex login status와 재부팅 후 timer를 확인합니다. updater 상태, session, Wine, keyring과 로그를 복사하지 않습니다. 끝 두 줄은 비활성화 선택 사항입니다.

```bash
git status --short
git switch main
git pull --ff-only origin main
git fetch --tags origin
./scripts/configure-updater.sh enable --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
./scripts/configure-updater.sh status
./scripts/configure-updater.sh disable
# 유지관리 설정과 모든 개인 상태까지 삭제하려면:
./scripts/configure-updater.sh disable --purge-state
```
