tfInYear = 3754;
tfInMonth = 4;
tfInDay = 1;
tfInHour = 14;
tfInMinute = 4;
tfInSecond = 5;
If [((tfInYear % 4 == 0) && (tfInYear % 100 !=
      0)) || (tfInYear % 400 == 0),
 tfCalendar = {31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
 tfDaysThisYear = 366;
 ,
 tfCalendar = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
 tfDaysThisYear = 365;
 ]
tfHoursThisYear = tfDaysThisYear*24;
tfMinutesThisYear = tfHoursThisYear*60;
tfSecondsThisYear = tfMinutesThisYear*60;
tfPastDays = 0;
tfPastMonths = tfInMonth - 1;
For [i = 1, (i <= Length[tfCalendar]) && (tfPastMonths > 0), i++,
  tfPastDays += tfCalendar[[i]];
  tfPastMonths --;
  ];
tfInYearDecimal =
  tfInYear + (tfPastDays + tfInDay - 1 )/tfDaysThisYear +
   tfInHour/tfHoursThisYear + tfInMinute/tfMinutesThisYear +
   tfInSecond/tfSecondsThisYear;
tfOutAllOerzkloeksWM =
  DateDifference[DateObject[{-753, 1, 1}, "Second", Automatic],
    DateObject[{tfInYear, tfInMonth, tfInDay, tfInHour, tfInMinute,
      tfInSecond}, "Second", Automatic],
    "Second"]*(9192631770/7909306972)/Quantity[1, "Seconds"];

tfRest = tfOutAllOerzkloeksWM;
tfOutYear = Floor[tfRest/(7*49*49*49*49)]
tfRest -= tfOutYear*(7*49*49*49*49);
tfOutMonth = Floor[tfRest/(49*49*49*49)]
tfRest -= tfOutMonth*(49*49*49*49);
tfOutDay = Floor[tfRest/(49*49*49)]
tfRest -= tfOutDay*(49*49*49);
tfOutHour = Floor[tfRest/(49*49)]
tfRest -= tfOutHour*(49*49);
tfOutMinute = Floor[tfRest/(49)]
tfRest -= tfOutMinute*49;
tfOutSecond = Floor[tfRest]
tfRest -= tfOutSecond;
