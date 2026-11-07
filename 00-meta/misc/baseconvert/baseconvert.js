/* Base Converter, urspruenglich erstellt fuer die Infinite Adventures     *
 * Hintergrund-Stil urspruenglich erstellt fuer tfrei.de/git               *
 * Die gesamte Datei ist gemeinfrei / public domain / CC0.                 *
 * Tobias Frei, 2019                                                       */

/* This is free and unencumbered software released into the public domain. */

/* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,         *
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF      *
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  *
 * IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR       *
 * OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,   *
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR   *
 * OTHER DEALINGS IN THE SOFTWARE.                                         */

const tfBaseX = document.getElementById('tf-basex');
const tfBase10 = document.getElementById('tf-base10');
tfBaseX.addEventListener('input', ConvertBase1);
tfBase10.addEventListener('input', ConvertBase2);

function ConvertBase1() {
    /* Base 10 -> Base X */
    var value1 = document.getElementById("value1").value;
    var base1 = document.getElementById("base1").value;
    document.getElementById("display1value").innerHTML = parseInt(value1, 10);
    document.getElementById("display1base").innerHTML = parseInt(base1, 10);
    document.getElementById("result1").innerHTML = parseInt(value1, 10).toString(parseInt(base1, 10)).toUpperCase();
}
function ConvertBase2() {
    /* Base X -> Base 10 */
    var value2 = document.getElementById("value2").value;
    var base2 = document.getElementById("base2").value;
    document.getElementById("display2value").innerHTML = parseInt(value2, parseInt(base2, 10)).toString(parseInt(base2, 10)).toUpperCase();
    document.getElementById("display2base").innerHTML = parseInt(base2, 10);
    document.getElementById("result2").innerHTML = parseInt(value2, parseInt(base2, 10));
}
