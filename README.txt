Names: Sydney Taylor, Kenton Carrier
URL: http://www.cs.uky.edu/~spta224/CS316/P1/P1_form.html
Description: This program is a General Conversion Calculator. For Part 1, the user can
submit two unit values and an amount. The program will return a table with the same units
and the amount when converted from the first unit to the second, or an error if this conversion
is not possible. For Part 2, the user can submit two unit values and the program will return the
path for conversion between the two or that there is no path.

Q1) What exactly does your CGI do if the value for myin and myout have the same units?

  If the values for myin and myout are the same, our CGI will print the value submitted for
  amount as the answer.

Q2) What is an example curl command to produce an answer? What answer did you receive?
Specifically,describe what you see from the output.

  curl "http://www.cs.uky.edu/~spta224/CS316/P1/universal.cgi?myin=usdollar&myout=euro&inamount=1&submit1=Make+it+so"

  <html><body><table border="1"><tr>
  <th>IN</th><th>OUT</th><th>QUANTITY</th><th>&nbsp;</th>
  <th>ANSWER/ERROR</th></tr><tr>
  <td>usdollar</td><td>euro</td>
  <td>1.0</td>
  <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
  <td style="color: ">0.88</td>
  </tr></table></body></html>

  The output displays the HTML form that our CGI is printing. However, instead of seeing the names 
  of our values (MyIn, MyOut, InAmount, conversion) we see the actual value that the form would 
  print on the browser (usdollar, euro, 1.0, 0.88). 

Q3) What happens (ie, what does the user see) if one of the field values submitted to your CGI
is a string of 100 characters? 1000 characters? 10000 characters?

  With 100 or 1000 characters, the user will just see a much longer table. With 10000 characters,
  the user will see an error, because the GET parameters make the URL too long.

Q4) The program "wc" with the "-l" option countsthe newline characters in a file.
If you were given 200 new unit conversion factors for more units using the CGI,
what would be the difference in the output of "wc -l" between your program and the new program?

  200 new lines, because each conversion is a line in our dictionary. The conversions aren't hard
  coded into our functions, so adding more doesn't affect anything outside the dictionary.
