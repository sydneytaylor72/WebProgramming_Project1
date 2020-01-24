#!/usr/bin/python
#Names: Sydney Taylor, Kenton Carrier
import cgi
import cgitb
import math

conversions = {
  "usdollar,euro": 0.88,
  "usdollar,xarn": 26.2,
  "usdollar,icekrona": 119.88,
  "xarn,polandzloty": 0.1434198,
  "icekrona,galacticrock": 0.001029839,
  "parsec,lightyear": 3.26,
  "lightyear,kilometer": 95000000000000,
  "lightyear,mile": 5886000000000,
  "xlarn,parsec": 7.3672,
  "galacticrock,terrestrialyear": 250000000,
  "xarnyear,terrestrialyear": 1.2579,
  "terrestrialyear,terrestrialminute": 525600,
  "bar,kilopascal": 100,
  "torr,kilopascal": 0.1333223684211,
  "psi,torr": 51.71487786825,
  "hour,second": 3600,
  "day,hour": 24,
  "hour,minute": 60
}

#Checks if unit is in the conversions dictionary
def checkUnitExist(unit):
  for key in conversions:
    if unit.lower() in key.split(","):
      return True
  return False

# Gets all conversions bidirectionally connected to the start parameter
def getConnections(start):
  connections = []
  for key in conversions:
    if start.lower() in key:
      units = key.split(",")
      for unit in units:
        if unit != start.lower():
          connections.append(unit)
  return connections

# Converts amount from the firstUnit to secondUnit if conversion exists in the
# dictionary
def convert(amount, firstUnit, secondUnit):
  # Check if both units exist in the conversions dictionary
  if checkUnitExist(firstUnit) == False:
    return "UNKNOWN CHOICE," + firstUnit
  elif checkUnitExist(secondUnit) == False:
    return "UNKNOWN CHOICE," + secondUnit

  #Checks if the two units given are identical
  if firstUnit == secondUnit:
    return amount

  # Create two possible conversion dictionary keys from input units
  forward = "%s,%s" % (firstUnit.lower(), secondUnit.lower())
  backward = "%s,%s" % (secondUnit.lower(), firstUnit.lower())

  # Calculate the conversion if its found, otherwise return NO PATH
  if forward in conversions:
    return amount * conversions.get(forward)
  elif backward in conversions:
    return amount / conversions.get(backward)
  else:
    return "NO PATH"

# Finds a 1-hop path between two denominations in the conversion table
# Returns the intersecting denomination or error message
def isPath(maybeIn, maybeOut):
  # Checks if the two parameters are the same
  if maybeIn.lower() == maybeOut.lower():
    return "SAME CHOICE"

  # Loop through the keys to find a direct path from maybeIn to maybeOut
  for key in conversions:
    if maybeIn.lower() in key and maybeOut.lower() in key:
      return maybeOut.lower()

  # Finds a 1-hop connection and returns the middleman or NO PATH if one isnt
  # found
  middleMan = set(getConnections(maybeIn)).intersection(getConnections(maybeOut))
  if middleMan:
    return middleMan.pop()
  else:
    return "NO PATH"

def main():
    cgitb.enable()
    print("Content-type:text/html\n\n")
    form = cgi.FieldStorage()
    answerColor = ""

    # Checks if the user clicked the first button
    if form.getvalue('submit1') == "Make it so":
      firstChoiceColor = ""
      secondChoiceColor = ""
      amountColor = ""
      conversion = ""
      MyIn = form.getvalue('myin')
      MyOut = form.getvalue('myout')
      InAmount = form.getvalue('inamount')

      # Checks if user has not submitted a value for MyIn
      if not MyIn:
        firstChoiceColor = "red"
        conversion = "UNKNOWN CHOICE"
        MyIn = "MISSING"
      # Checks if user has not submitted a value for MyOut
      if not MyOut:
        secondChoiceColor = "red"
        conversion = "UNKNOWN CHOICE"
        MyOut = "MISSING"
      # Checks if user has not submitted a value for InAmount
      if not InAmount:
        amountColor = "red"
        conversion = "UNKNOWN CHOICE"
        InAmount = "MISSING"

      # Try to convert InAmount to a float. If this throws an exception,
      # if this throws an exception set conversion and colors. If it does not
      # throw an exception, set InAmount
      try: float(InAmount)
      except:
        conversion = "NaN"
        answerColor = "red"
        amountColor = "red"
      else: InAmount = float(InAmount)

      # Check if both units exist in the conversions dictionary
      if MyIn != "MISSING" and checkUnitExist(MyIn.lower()) == False:
        conversion = "UNKNOWN CHOICE"
        firstChoiceColor = "blue"
        answerColor = "red"
      if MyOut != "MISSING" and checkUnitExist(MyOut.lower()) == False:
        conversion = "UNKNOWN CHOICE"
        secondChoiceColor = "blue"
        answerColor = "red"

      # Checks if conversion is not a number and not an unknown choice,
      # then calls the convert function
      if conversion != "NaN" and conversion != "UNKNOWN CHOICE":
        MyIn = MyIn.lower()
        MyOut = MyOut.lower()
        conversion = convert(InAmount, MyIn, MyOut)
        # Check if there is not a path between the two submitted values
        if conversion == "NO PATH":
          answerColor = "red";

      # Print an HTML table with the values from the first part of the form
      # and the conversion or applicable error
      print('<html><body><table border="1"><tr>')
      print('<th>IN</th><th>OUT</th><th>QUANTITY</th><th>&nbsp;</th>')
      print('<th>ANSWER/ERROR</th></tr><tr>')
      print ('<td style="color: %s">' + MyIn + '</td><td style="color: %s">' + MyOut + '</td>') % (firstChoiceColor, secondChoiceColor)
      print ('<td style="color: %s">%s</td>') %(amountColor, InAmount)
      print ('<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>')
      print ('<td style="color: %s">%s</td>') %(answerColor, conversion)
      print ('</tr></table></body></html>')

    # Checks if the user clicked the second button
    elif form.getvalue('submit2') == "Is path?":
      answerColor = "green"
      firstChoiceColor = ""
      secondChoiceColor = ""
      Path = ""
      MaybeIn = form.getvalue('maybein')
      MaybeOut = form.getvalue('maybeout')

      # Checks if user has not submitted a value for MaybeIn
      if not MaybeIn:
        firstChoiceColor = "red"
        Path = "UNKNOWN CHOICE"
        MaybeIn = "MISSING"
      # Checks if user has not submitted a value for MaybeOut
      if not MaybeOut:
        secondChoiceColor = "red"
        Path = "UNKNOWN CHOICE"
        MaybeOut = "MISSING"

      # Check if both units exist in the conversions dictionary
      if MaybeIn != "MISSING" and checkUnitExist(MaybeIn.lower()) == False:
        Path = "UNKNOWN CHOICE"
        firstChoiceColor = "blue"
      if MaybeOut != "MISSING" and checkUnitExist(MaybeOut.lower()) == False:
        Path = "UNKNOWN CHOICE"
        secondChoiceColor = "blue"

      # Checks if path is not an unknown choice, and then calls the isPath function
      if Path != "UNKNOWN CHOICE":
        MaybeIn = MaybeIn.lower()
        MaybeOut = MaybeOut.lower()
        Path = isPath(MaybeIn, MaybeOut)
      # Checks if there is no path or if the path is an unknown choice 
      if Path == "NO PATH" or Path == "UNKNOWN CHOICE":
        answerColor = "red";

      # Prints an HTML table with the values from the second part of the form
      # and the path or applicable error
      print ('<html><body><table border="1"><tr>')
      print ('<th>MAYBEIN</th><th>MAYBEOUT</th>')
      print ('<th>ANSWER/NOPATH</th><tr>')
      print ('<td style="color: %s">' + MaybeIn + '</td><td style="color: %s">' + MaybeOut + '</td>') % (firstChoiceColor, secondChoiceColor)
      print ('<td style="color: %s">' + Path + '</td>') % (answerColor)
      print ('</tr></table></body></html>')

    # Prints Invalid if the user changes the URL to not click either button
    else:
      print ('<html><body>')
      print ("Invalid")
      print ('</body></html>')

if __name__ == "__main__":
    main()
