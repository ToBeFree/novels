/* AeUeCalendar, urspruenglich erstellt fuer die Infinite Adventures       *
 * Die gesamte Datei ist gemeinfrei / public domain / CC0.                 *
 * Tobias Frei, 2022                                                       */

/* This is free and unencumbered software released into the public domain. */

/* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,         *
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF      *
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  *
 * IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR       *
 * OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,   *
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR   *
 * OTHER DEALINGS IN THE SOFTWARE.                                         */

var tfUtcForm = document.getElementById('tf-utc-form');
var tfAucForm = document.getElementById('tf-auc-form');
const tfSecondsPerOerzkloek = 7909306972/9192631770;
const tfSecondsPerOerzbit = 343*49*49*49*tfSecondsPerOerzkloek;

tfUtcForm.addEventListener('input', tfConvertUtcAuc);
tfAucForm.addEventListener('input', tfConvertAucUtc);

function tfConvertUtcAuc() {
    /* UTC -> AUC */
    var tfInYear = parseInt(document.getElementById("tf-utc-year-input").value, 10);
    var tfInMonth = parseInt(document.getElementById("tf-utc-month-input").value, 10);
    var tfInDay = parseInt(document.getElementById("tf-utc-day-input").value, 10);
    var tfInHour = parseInt(document.getElementById("tf-utc-hour-input").value, 10);
    var tfInMinute = parseInt(document.getElementById("tf-utc-minute-input").value, 10);
    var tfInSecond = parseInt(document.getElementById("tf-utc-second-input").value, 10);
    if (((tfInYear % 4 == 0) && (tfInYear % 100 != 0)) || (tfInYear % 400 == 0)) { /* leap year */
        var tfCalendar = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        var tfDaysThisYear = 366;
    } else {
        var tfCalendar = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        var tfDaysThisYear = 365;
    }
    var tfHoursThisYear = tfDaysThisYear*24;
    var tfMinutesThisYear = tfHoursThisYear*60;
    var tfSecondsThisYear = tfMinutesThisYear*60;
    var tfPastDays = 0;
    var tfPastMonths = tfInMonth-1; /* Months start at 1, so "1" means no month has passed and "12" means 11 have passed. */
    for (let i=0; (i<tfCalendar.length) && (tfPastMonths > 0); i++) {
        tfPastDays += tfCalendar[i];
        tfPastMonths --;
    };

    var tfInYearDecimal = tfInYear + (tfPastDays+tfInDay-1 /* Days start at 1 as well. */)/tfDaysThisYear + tfInHour/tfHoursThisYear + tfInMinute/tfMinutesThisYear + tfInSecond/tfSecondsThisYear;
    var tfOutYearDecimal = (tfSecondsAbUrbeCondita(tfInYear)+(tfPastDays+tfInDay-1)*24*60*60+tfInHour*60*60+tfInMinute*60+tfInSecond)/tfSecondsPerOerzbit;

    /* Exporting to AUC is simple as there are no leap years, each month has the same length and all fields start at 0. */
    var tfRest = tfOutYearDecimal; /* e.g. 2033.4029528 */
    var tfOutYear = Math.floor(tfOutYearDecimal); /* e.g. 2033 */
    tfRest -= tfOutYear; /* e.g. 0.4029528 */
    var tfOutMonth = Math.floor(tfRest*7); /* AUC years have 7 months */
    tfRest -= tfOutMonth/7;
    var tfOutDay = Math.floor(tfRest*343); /* AUC years have 343 days */
    tfRest -= tfOutDay/343;
    var tfOutHour = Math.floor(tfRest*343*49); /* AUC days have 49 hours */
    tfRest -= tfOutHour/(343*49);
    var tfOutMinute = Math.floor(tfRest*343*49*49); /* AUC hours have 49 minutes */
    tfRest -= tfOutMinute/(343*49*49);
    var tfOutSecond = Math.floor(tfRest*343*49*49*49); /* AUC minutes have 49 seconds */
    tfRest -= tfOutSecond/(343*49*49*49);

    document.getElementById("tf-utc-year-inputecho").innerHTML = tfInYear;
    document.getElementById("tf-utc-month-inputecho").innerHTML = tfInMonth;
    document.getElementById("tf-utc-day-inputecho").innerHTML = tfInDay;
    document.getElementById("tf-utc-hour-inputecho").innerHTML = tfInHour;
    document.getElementById("tf-utc-minute-inputecho").innerHTML = tfInMinute;
    document.getElementById("tf-utc-second-inputecho").innerHTML = tfInSecond;
    document.getElementById("tf-utc-yeardecimal-inputecho").innerHTML = tfInYearDecimal;
    document.getElementById("tf-auc-year-output").innerHTML = tfOutYear;
    document.getElementById("tf-auc-month-output").innerHTML = tfOutMonth;
    document.getElementById("tf-auc-day-output").innerHTML = tfOutDay;
    document.getElementById("tf-auc-hour-output").innerHTML = tfOutHour;
    document.getElementById("tf-auc-minute-output").innerHTML = tfOutMinute;
    document.getElementById("tf-auc-second-output").innerHTML = tfOutSecond;
    document.getElementById("tf-auc-yeardecimal-output").innerHTML = tfOutYearDecimal;
}

function tfConvertAucUtc() {
    /* AUC -> UTC */
    var tfInYear = parseInt(document.getElementById("tf-auc-year-input").value, 10);
    var tfInMonth = parseInt(document.getElementById("tf-auc-month-input").value, 10);
    var tfInDay = parseInt(document.getElementById("tf-auc-day-input").value, 10);
    var tfInHour = parseInt(document.getElementById("tf-auc-hour-input").value, 10);
    var tfInMinute = parseInt(document.getElementById("tf-auc-minute-input").value, 10);
    var tfInSecond = parseInt(document.getElementById("tf-auc-second-input").value, 10);

    /* Importing from AUC is simple as there are no leap years, each month has the same length and all fields start at 0. */
    var tfInYearDecimal = tfInYear + tfInMonth/7 + tfInDay/343 + tfInHour/(343*49) + tfInMinute/(343*49*49) + tfInSecond/(343*49*49*49);
    var tfPastSeconds = (tfInYear*343*49*49*49 + tfInMonth*49*49*49*49 + tfInDay*49*49*49 + tfInHour*49*49 + tfInMinute*49 + tfInSecond)*tfSecondsPerOerzkloek;

    var tfRest = tfPastSeconds;
    var tfOutYear = (-752);
    var tfOutYearDecimal = tfOutYear;
    var tfOutMonth = 0;
    var tfOutDay = 0;
    var tfOutHour = 0;
    var tfOutMinute = 0;
    var tfOutSecond = 0;
    var tfLoopBegin = Math.min(tfPastSeconds, 0);
    var tfLoopEnd = Math.max(tfPastSeconds, 0);
    var tfLoopSign = Math.sign(tfPastSeconds-0);
    var tfFebDays = 29;
    var tfDaysThisYear = 366;
    while (tfRest > tfDaysThisYear*24*60*60) { /* over 1 year left */
        tfOutYear ++;
        tfOutYearDecimal ++;
        tfRest -= tfDaysThisYear*24*60*60;
        console.log(tfRest);
        if (((tfOutYear % 4 == 0) && (tfOutYear % 100 != 0)) || (tfOutYear % 400 == 0)) { /* leap year */
            tfFebDays = 29;
            tfDaysThisYear = 366;
        } else {
            tfFebDays = 28;
            tfDaysThisYear = 365;
        }
    }
    tfOutYearDecimal += tfRest/(tfDaysThisYear*24*60*60);

    var tfCalendar = [31, tfFebDays, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    for (let m=0; (m<tfCalendar.length) && (tfRest > tfCalendar[m]*24*60*60); m++) { /* over 1 month left */
        tfOutMonth ++;
        tfRest -= tfCalendar[m]*24*60*60;
    }

    tfOutDay += Math.floor(tfRest/(24*60*60));
    tfRest -= tfOutDay*(24*60*60);
    tfOutHour += Math.floor(tfRest/(60*60));
    tfRest -= tfOutHour*(60*60);
    tfOutMinute += Math.floor(tfRest/60);
    tfRest -= tfOutMinute*60;
    tfOutSecond += Math.floor(tfRest);
    tfRest -= tfOutSecond;

    tfOutMonth += 1; /* Displayed month number starts at 1 */
    tfOutDay += 1; /* Displayed day number starts at 1 */

    document.getElementById("tf-auc-year-inputecho").innerHTML = tfInYear;
    document.getElementById("tf-auc-month-inputecho").innerHTML = tfInMonth;
    document.getElementById("tf-auc-day-inputecho").innerHTML = tfInDay;
    document.getElementById("tf-auc-hour-inputecho").innerHTML = tfInHour;
    document.getElementById("tf-auc-minute-inputecho").innerHTML = tfInMinute;
    document.getElementById("tf-auc-second-inputecho").innerHTML = tfInSecond;
    document.getElementById("tf-auc-yeardecimal-inputecho").innerHTML = tfInYearDecimal;
    document.getElementById("tf-utc-year-output").innerHTML = tfOutYear;
    document.getElementById("tf-utc-month-output").innerHTML = tfOutMonth;
    document.getElementById("tf-utc-day-output").innerHTML = tfOutDay;
    document.getElementById("tf-utc-hour-output").innerHTML = tfOutHour;
    document.getElementById("tf-utc-minute-output").innerHTML = tfOutMinute;
    document.getElementById("tf-utc-second-output").innerHTML = tfOutSecond;
    document.getElementById("tf-utc-yeardecimal-output").innerHTML = tfOutYearDecimal;
}

function tfSecondsAbUrbeCondita(tfInYear) {
    /* How many seconds have passed between the start of "-752" and the start of the current year? */
    var tfOutSeconds = 0;
    var tfLoopBegin = Math.min(tfInYear, (-752));
    var tfLoopEnd = Math.max(tfInYear, (-752));
    var tfLoopSign = Math.sign(tfInYear-(-752));
    for (let y=tfLoopBegin; y<tfLoopEnd; y++) {
        if (((y % 4 == 0) && (y % 100 != 0)) || (y % 400 == 0)) { /* leap year */
            tfOutSeconds += 366*24*60*60;
        } else {
            tfOutSeconds += 365*24*60*60;
        }
    };
    return tfLoopSign*tfOutSeconds;
}
