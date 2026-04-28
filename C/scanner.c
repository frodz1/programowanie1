#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Structure {
        char *name;
        char *language;
        char *id;
        char *bio;
        char *version;

};


void skaner(char *zmienna, char *buf){

	int dziala = 1;
	

	for (int i = 1; 1; i++){
	  scanf("%c", &buf[i]);

	  if (buf[i] == ']') {
		dziala = 0;	
		break;		  
	}

	  if (buf[i-1] == ':'  && buf[i] == ' ')
	  {
	    break;
	  }	
	}

	if (dziala == 1) {

	scanf("%c", buf);
	for (int i = 0; 1; i++){
	  scanf("%c", &zmienna[i]);
	  if (i!=0 && zmienna[i-1] == '"'  && zmienna[i] == ',')
	  {
	    zmienna[i-1] = '\0';
	    break;
	  }	
	}
	}
	
}

void get_version(char *zmienna, char *buf){

        scanf("%s", buf);
        scanf("%c", buf);
	scanf("%s", zmienna);

}

struct Structure stworz_strukture(void) {
	
	struct Structure s;

	char *trash = malloc(1024);
        s.name = malloc(1024);
        s.language=malloc(1024);
        s.id = malloc((1024));           
        s.bio = malloc(1024);
        s.version = malloc(128);

	skaner(s.name, trash);
	skaner(s.language, trash);
	skaner(s.id, trash);
	skaner(s.bio, trash);

	get_version(s.version, trash);

	return s;


}

void printowanie_struktury(struct Structure s) {

printf("  {\n    \"name\": \"%s\",\n    \"language\": \"%s\",\n    \"id\": \"%s\",\n    \"bio\": \"%s\",\n    \"version\": %s\n  },\n",
         s.name, s.language, s.id, s.bio, s.version);

}	


void ostatnia_struktura(struct Structure s) {

printf("  {\n    \"name\": \"%s\",\n    \"language\": \"%s\",\n    \"id\": \"%s\",\n    \"bio\": \"%s\",\n    \"version\": %s\n  }\n",
         s.name, s.language, s.id, s.bio, s.version);

}	

int main() {
      
	int size = 100;

	struct Structure *tab = malloc(size * sizeof(struct Structure));

	if (tab == NULL) {
	printf("\nMalloc mial problem");
	exit(1);
	}

	for (int i=0; i<size; i++){
	
	   if(i == size - 1) {
		size = size * 2;
		tab = realloc(tab, size * sizeof(struct Structure));
		if (tab==NULL) {
			printf("Realloc zaliczył problem");
			exit(1);
		}
		}
		
	tab[i] = stworz_strukture();
       	if (feof(stdin) || ferror(stdin)) {
		size = i - 1;
		break;
	}
	}
	printf("[\n");
	for (int i=0; i<=size; i++){
	
	if (i < size){	
		printowanie_struktury(tab[i]);
		
	}else{
		ostatnia_struktura(tab[i]);
	}
	}

	printf("]\n");

	return 0;

}

