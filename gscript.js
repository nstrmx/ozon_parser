// Скрипт для google таблиц
var ss      = SpreadsheetApp.getActiveSpreadsheet();
var list1   = getList("Лист1");

function getList(name){
  return ss.getSheetByName(name);
}

function calc_diff () {
    var 
        new_price  = list1.getRange("C2:C").getValues(),
        old_price  = list1.getRange("D2:D").getValues(),
        difference = list1.getRange("H2:H"),
        percent    = list1.getRange("I2:I"),
        cell_a, cell_b, val_a, val_b,
        i;

    var diff_values = []
    var perc_values = []

    for (i = 0; i < new_price.length; i++) {
        cell_a = new_price[i][0]
        cell_b = old_price[i][0]
        if (cell_a && cell_b) {
            val_a = parseInt(cell_a.replace(/(₽|\s)/, ""))
            val_b = parseInt(cell_b.replace(/(₽|\s)/, ""))

            diff_values.push([val_a - val_b])
            perc_values.push([(100 - Math.round(val_a / val_b * 100)) + "%"])
        }
        else {
            diff_values.push([""])
            perc_values.push([""])
        }
        
    }

    difference.setValues(diff_values)
    percent.setValues(perc_values)
}

function onOpen () {
  calc_diff()
}
