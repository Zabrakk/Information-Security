#include <stdio.h>
#include <stdlib.h>

#define MAX_LEN 100
#define OUTPUT_NAME "encrypted.txt"

void rot13(char*);
void encrypt_file(char*);

void main() {
	char file_name[32];
	char text[100];
	char opt[3]; // 1\n\0


	printf("Note that max length of file name is 31 characters!\n");
	printf("Max length of text stings are 99 charters\n\n");
	printf("Do you want to 1. encrypt text 2. encrypt a file? ");
	fgets(opt, 3, stdin);

	if (opt[0] == '1') {
		printf("Enter a message to encrypt: ");
		fgets(text, MAX_LEN, stdin);
		rot13(&text);
		printf("%s\n", text);
	} else if (opt[0] == '2') {
		printf("#: Enter a file to encrypt: ");
		fgets(file_name, MAX_LEN, stdin);
		printf("%s\n", file_name);
		encrypt_file(&file_name);
	} else {
		printf("Unknown command\n");
	}

	system("pause");
}

//Takes a filename as an argument, opens the file reads all lines and encrypts them with the rot13() function writes output to new file
void encrypt_file(char* file_name) {
	file_name[strlen(file_name) - 1] = '\0'; //Remove new line from strings end
	FILE *input = fopen(file_name, "r");
	char line[100];

	if (input == NULL) {
		printf("#: File not found, exiting");
		system("pause");
	}
	FILE *output = fopen(OUTPUT_NAME, "w");
	printf("#: Starting encryption\n");
	while (fgets(line, sizeof(line), input) != NULL) {
		rot13(&line);
		fprintf(output, "%s", line);
	}
	printf("#: Encryption completed\n");
}

//Shifts letters by 13
void rot13(char* msg) {
	for (int i = 0; i < strlen(msg); i++) {
		if (msg[i] == ' ') {
			printf(" ");
		} else if ((msg[i] >= 'a' && msg[i] <= 'm') || (msg[i] >= 'A' && msg[i] <= 'M')) {
			msg[i] = msg[i] + 13;
		}
		else if ((msg[i] >= 'n' && msg[i] <= 'z') || (msg[i] >= 'N' && msg[i] <= 'Z')) {
			msg[i] = msg[i] - 13;
		}
	}
}