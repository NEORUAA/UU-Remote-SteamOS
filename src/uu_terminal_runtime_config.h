#ifndef UURB_TERMINAL_RUNTIME_CONFIG_H
#define UURB_TERMINAL_RUNTIME_CONFIG_H

/* Shared exact managed runtime handoff for the proxy and UU pipe adapter. */
static int parse_port(const char *value, uint16_t *port)
{
    char *end = NULL;
    unsigned long parsed;

    if (value == NULL || *value == '\0')
        return 0;
    parsed = strtoul(value, &end, 10);
    if (*end != '\0' || parsed == 0 || parsed > 65535)
        return 0;
    *port = (uint16_t)parsed;
    return 1;
}

static int token_is_valid(const char *token)
{
    size_t index;

    if (token == NULL || strlen(token) != UURB_TERMINAL_TOKEN_LENGTH)
        return 0;
    for (index = 0; index < UURB_TERMINAL_TOKEN_LENGTH; index++) {
        if (!((token[index] >= '0' && token[index] <= '9') ||
              (token[index] >= 'a' && token[index] <= 'f')))
            return 0;
    }
    return 1;
}

static int load_environment_configuration(char *token, uint16_t *port)
{
    char port_text[16];
    DWORD token_length;
    DWORD port_length;

    token_length = GetEnvironmentVariableA(
        "UURB_TERMINAL_BRIDGE_TOKEN", token,
        UURB_TERMINAL_TOKEN_LENGTH + 1);
    port_length = GetEnvironmentVariableA(
        "UURB_TERMINAL_BRIDGE_PORT", port_text, sizeof(port_text));
    return token_length == UURB_TERMINAL_TOKEN_LENGTH &&
           port_length > 0 && port_length < sizeof(port_text) &&
           token_is_valid(token) && parse_port(port_text, port);
}

static int runtime_configuration_path(char *path, size_t path_size)
{
    char *backslash;
    char *separator;
    char *slash;
    DWORD length;
    size_t directory_length;
    size_t filename_length = strlen(UURB_TERMINAL_CONFIG_FILENAME);

    length = GetModuleFileNameA(NULL, path, (DWORD)path_size);
    if (length == 0 || length >= path_size)
        return 0;
    backslash = strrchr(path, '\\');
    slash = strrchr(path, '/');
    separator = backslash;
    if (slash != NULL && (separator == NULL || slash > separator))
        separator = slash;
    if (separator == NULL)
        return 0;
    directory_length = (size_t)(separator - path) + 1;
    if (directory_length + filename_length + 1 > path_size)
        return 0;
    memcpy(path + directory_length, UURB_TERMINAL_CONFIG_FILENAME,
           filename_length + 1);
    return 1;
}

static BOOL runtime_persistent;

static int load_runtime_configuration(char *token, uint16_t *port)
{
    static const char prefix[] = "version=1\nport=";
    char config[256];
    char path[32768];
    char port_text[16];
    char *cursor;
    char *newline;
    DWORD received;
    HANDLE file = INVALID_HANDLE_VALUE;
    LARGE_INTEGER size;
    size_t port_length;
    int result = 0;

    runtime_persistent = FALSE;

    if (!runtime_configuration_path(path, sizeof(path)))
        goto done;
    file = CreateFileA(path, GENERIC_READ,
                       FILE_SHARE_READ | FILE_SHARE_DELETE, NULL,
                       OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (file == INVALID_HANDLE_VALUE ||
        !GetFileSizeEx(file, &size) || size.QuadPart <= 0 ||
        size.QuadPart >= (LONGLONG)sizeof(config) ||
        !ReadFile(file, config, (DWORD)size.QuadPart, &received, NULL) ||
        received != (DWORD)size.QuadPart)
        goto done;
    config[received] = '\0';
    if (strncmp(config, prefix, sizeof(prefix) - 1) != 0)
        goto done;
    cursor = config + sizeof(prefix) - 1;
    newline = strchr(cursor, '\n');
    if (newline == NULL)
        goto done;
    port_length = (size_t)(newline - cursor);
    if (port_length == 0 || port_length >= sizeof(port_text))
        goto done;
    memcpy(port_text, cursor, port_length);
    port_text[port_length] = '\0';
    cursor = newline + 1;
    if (strncmp(cursor, "token=", 6) != 0)
        goto done;
    cursor += 6;
    if (strlen(cursor) < UURB_TERMINAL_TOKEN_LENGTH + 1 ||
        cursor[UURB_TERMINAL_TOKEN_LENGTH] != '\n')
        goto done;
    const char *mode = cursor + UURB_TERMINAL_TOKEN_LENGTH + 1;
    if (*mode && strcmp(mode, "session_mode=persistent\n") &&
        strcmp(mode, "session_mode=fresh\n")) goto done;
    memcpy(token, cursor, UURB_TERMINAL_TOKEN_LENGTH);
    token[UURB_TERMINAL_TOKEN_LENGTH] = '\0';
    result = token_is_valid(token) && parse_port(port_text, port);
    runtime_persistent = result && !strcmp(mode, "session_mode=persistent\n");

done:
    if (file != INVALID_HANDLE_VALUE)
        CloseHandle(file);
    SecureZeroMemory(config, sizeof(config));
    SecureZeroMemory(path, sizeof(path));
    SecureZeroMemory(port_text, sizeof(port_text));
    if (!result)
        SecureZeroMemory(token, UURB_TERMINAL_TOKEN_LENGTH + 1);
    return result;
}

static int load_configuration(char *token, uint16_t *port)
{
    if (load_environment_configuration(token, port))
        return 1;
    SecureZeroMemory(token, UURB_TERMINAL_TOKEN_LENGTH + 1);
    return load_runtime_configuration(token, port);
}

#endif
