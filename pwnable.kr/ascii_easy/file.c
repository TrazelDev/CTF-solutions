#include <unistd.h>

extern char **environ;
int main() {
	execle("sh;", "fafafafa", NULL, NULL);
}
