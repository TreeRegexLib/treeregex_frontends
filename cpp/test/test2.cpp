#include <stdio.h>

int get_error_term();

int foo(){
	int baz = get_baz();

	if(baz == 3){
		return 1;
	} else if (baz = get_error_term()){
		printf("Error!\n");
	} else {
		return 0;
	}
}
