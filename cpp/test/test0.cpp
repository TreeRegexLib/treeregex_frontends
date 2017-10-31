void really_slow_function(int i);

int main(){
	int m ;
	for(int i = 0; i < 10; --i){
		if(i%2 == 0){
			really_slow_function(1000);
		}
	}
}
