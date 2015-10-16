#include <stdio.h>

/******************
 * tt2ht1.c
 ******************
 * This program transforms a white-space delimited unix text table into an html table.
 * input: text table
 * output: html table
 * by Tom Lehmann
 ******************/

#define MAXLEN 100 //The maximum length allowed for an input line

void printLine(char[],int); 

/* main method 
 * Scanes through standard input until reaching EOF.
 * Places each line into a char array.
 * Once reaching a newline character, executes printLine and passes the char array.
 */
int main(void)
{
  char c;
  int lineMarker = 0;
  char line[MAXLEN];

  printf("  <table>\n"); //print the table header

  while( (c=getchar()) != EOF) //loops until EOF
  {

    line[lineMarker] = c; //copy the current char into the array
    if (c == '\n') //if at new line, call printLine and reset lineMarker
    {
      printLine(line,lineMarker);
      lineMarker = 0; 
    } else 
    {
      lineMarker++;
      if(lineMarker >= 100) //bail if the line is too long
      {
        printf("Line is too long.  Exiting.\n");
        break;
      }
    }
  }
 
  printf("  </table>\n"); //print the table footer 

  return 0;
}

/* printLine
 * input: character array and integer of the arrays length
 * returns: nothing 
 * prints: the line as an row in a html table
 */
void printLine(char ch[], int lineLen)
{
  int i, inElement;
  inElement = 1; //marker to tell if scanning over element or not
  printf("    <tr>\n"); //print the opening tags
  printf("      <td>");
  for (i = 0; i < lineLen; i++) //loop over all chars in the line
  {
    if(inElement == 1 && isspace(ch[i])) //if we reach a whitespace while in an element, print a closing tag
    {
      printf("</td> ");
      inElement = 0;  
    }
    else if(inElement == 1 && !isspace(ch[i])) //if we are in an element, print the char
    {
      putchar(ch[i]);
    }
    else if(inElement == 0 && !isspace(ch[i])) //if we are outside an elent and reach one, print an opening tag
    {
      printf("<td>");
      putchar(ch[i]);
      inElement = 1;
    }
    else {
    }
  }
  printf("</td>"); //print the closing tags
  printf("\n    </tr>\n");
}
