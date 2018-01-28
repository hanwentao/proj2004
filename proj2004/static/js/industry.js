$(function() {
  function createOptions(field, choices) {
    field.append("<option value>---------</option>");
    for (var choice of choices) {
      $(`<option value="${choice}">${choice}</option>`).appendTo(field);
    }
  }

  function updateSpecify(masterField, slaveField) {
    var masterValue = masterField.val();
    if (masterValue == "其他" || masterValue == "Other") {
      slaveField.show();
    } else {
      slaveField.hide();
    }
  }

  function initState(fields, values) {
    fields[0].val(values[0]);
    updateSpecify(fields[0], fields[1]);
  }

  function updateState(fields, oldValues) {
    var newValues = [fields[0].val(), fields[1].val()];
    if (newValues[0] != oldValues[0]) {
      fields[1].val("");
      updateSpecify(fields[0], fields[1]);
    }
    oldValues[0] = newValues[0];
    oldValues[1] = newValues[1];
  }

  var name = "industry";
  var id = `id_${name}`;
  var selectField = $(`#${id}_0`);
  var specifyField = $(`#${id}_1`);
  var values = [selectField.val(), specifyField.val()];
  selectField.replaceWith(`<select name="${name}_0" class="form-control" title id="${id}_0"></select>`);
  selectField = $(`#${id}_0`);
  var fields = [selectField, specifyField];
  createOptions(selectField, industryChoices);
  selectField.change(function() {
    updateState(fields, values);
  });
  initState(fields, values);
});
