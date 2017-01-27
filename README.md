# Markov
<\n>
By default reads lines of text from standard input and generates one new piece of text from those lines as output.
<\n>
Options: <\n>
  -n use to create more output (e.g. -n 5 for 5 lines)<\n>
  -f read text from a file (e.g. -f test.txt)<\n>
  -s change what the separator used to split each line into words (default single space)<\n>
  -l length of prefix to generate new text based on. <\n>
      short - 1 word is used to pick out what the next word is   (e.g. it sees what words follow "bear" and picks one at random)<\n>
      long - 2 words are used to pick out what the next word is  (e.g. it sees what words follow "bear eats" and picks one at random)<\n>
      hybrid - tries to use two words but will go with one word if there's only one option for what follows the two-word combo<\n>
  -t specify how to clean the text to create more possibilities for what follows<\n>
      lower - takes each word to lower case<\n>
      nopunc - lowers the text and removes punctuation
  
  
