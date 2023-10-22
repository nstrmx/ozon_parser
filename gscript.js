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
            val_a = parseInt(cell_a)
            val_b = parseInt(cell_b)

            max_val = Math.max(val_a, val_b)
            min_val = Math.min(val_a, val_b)

            diff_values.push([max_val - min_val])
            perc_values.push([(100 - Math.round(min_val / max_val * 100)) + "%"])
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
