#include <stdio.h>
#include <string.h>
#include <ncurses.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/select.h>
#include <arpa/inet.h>

#define SWITCH_MAGIC '$'

static bool ncurses_mode = false;

static void init_ncurses(void)
{
    initscr();
    raw();
    keypad(stdscr, TRUE);
    noecho();
    resizeterm(24, 80);
    ncurses_mode = true;
}

static int open_socket(const char *ip, int port)
{
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd == -1) {
        perror("socket");
        exit(1);
    }

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);

    int ret = inet_pton(AF_INET, ip, &addr.sin_addr);
    if (ret == 0) {
        fprintf(stderr, "ERROR: invalid IP address\n");
        exit(1);
    }
    if (ret == -1) {
        perror("inet_pton");
        exit(1);
    }

    if (connect(fd, (struct sockaddr *)&addr, sizeof(addr)) == -1) {
        perror("connect");
        exit(1);
    }

    return fd;
}

static void write_exactly(int fd, const void *buf, size_t count)
{
    const char *ptr = (const char *)buf;
    while (count) {
        ssize_t num = write(fd, ptr, count);
        if (num == -1) {
            perror("write");
            exit(1);
        }
        count -= num;
        ptr += num;
    }
}

static void proxy_stdio(int fd)
{
    while (true) {
        fd_set rfds;
        FD_ZERO(&rfds);
        FD_SET(STDIN_FILENO, &rfds);
        FD_SET(fd, &rfds);

        if (select(fd+1, &rfds, NULL, NULL, NULL) == -1) {
            perror("select");
            exit(1);
        }

        int src_fd = -1, dst_fd = -1;
        if (FD_ISSET(STDIN_FILENO, &rfds)) {
            src_fd = STDERR_FILENO;
            dst_fd = fd;
        } else if (FD_ISSET(fd, &rfds)) {
            src_fd = fd;
            dst_fd = STDOUT_FILENO;
        }

        char buf[1000];
        ssize_t num = read(src_fd, buf, sizeof(buf));
        if (num == -1) {
            perror("read");
            exit(1);
        }
        if (num == 0)
            break;

        if (!ncurses_mode && src_fd == fd) {
            for (size_t i = 0; i < num; i++) {
                if (buf[i] == SWITCH_MAGIC) {
                    write_exactly(dst_fd, buf, i + 1);
                    init_ncurses();
                    write_exactly(dst_fd, buf + i + 1, num - i - 1);
                    num = 0;
                    break;
                }
            }
        }

        write_exactly(dst_fd, buf, num);
    }
}

int main(int argc, char *argv[])
{
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <IP> <port>\n", argv[0]);
        return 1;
    }

    int fd = open_socket(argv[1], atoi(argv[2]));
    proxy_stdio(fd);

    if (ncurses_mode)
        endwin();
}
