$(function() {
  var updateState = function() {
    var selectField = $("#id_industry_0");
    var specifyField = $("#id_industry_1");
    var value = selectField.val();
    if (value == "其他") {
      specifyField.show();
    } else {
      specifyField.hide();
    }
  };
  var selectField = $("#id_industry_0");
  var specifyField = $("#id_industry_1");
  var value = selectField.val();
  selectField.replaceWith(`<select name="industry_0" class="form-control" title id="id_industry_0"></select>`);
  selectField = $("#id_industry_0");
  selectField.append("<option value>---------</option>");
  for (var choice of industryChoices) {
    var option = $(`<option value="${choice}">${choice}</option>`).appendTo(selectField);
    if (choice == value) {
      option.attr("selected", "selected");
    }
  }
  updateState();
  selectField.change(function() {
    updateState();
  });
});
