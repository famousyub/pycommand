#include <stdio.h>


#include<stdlib.h>
#include <windows.h>


void _telnet(const char *_ip)
{

    char buff[1024];
    sprintf(buff,"telnet %s" ,_ip);
     FILE *fp = popen(buff,"w");

   fprintf(fp, "Menara\n");
   fprintf(fp, "Menara\n");
   fprintf(fp, "PAUSE\n");

   if (pclose(fp) != 0) {
       /* Error reported by pclose() */
       fprintf (stderr, "Could not run more or other error.\n");
   }

   return ;
}
int main() {


  FILE *fptr;

  // Open a file in read mode
  _telnet("192.168.5.1");
  fptr = fopen("commande.txt", "r");
  system("ping 192.168.5.1 ");

  // Store the content of the file
  char myString[100];

  // If the file exist
  if(fptr != NULL) {
  
    // Read the content and print it
    while(fgets(myString, 100, fptr)) {
      printf("%s", myString);
    }
    
  // If the file does not exist 
  } else {
    printf("Not able to open the file.");
  }

  // Close the file
  fclose(fptr);

  return 0;
}