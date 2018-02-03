$(function() {
  function createOptions(field, choices, value) {
    if (!choices) {
      return;
    }
    field.empty();
    field.append("<option value>---------</option>");
    for (var choice of choices) {
      field.append(`<option value="${choice}">${choice}</option>`);
    }
    if (value != undefined) {
      field.val(value);
    }
    field.show();
  }

  function checkSpecify(node, data) {
    var value = node.field.val();
    if (value === "其他" || value === "Other") {
      return true;
    }
    return false;
  }

  function initState(node, data, clearValue) {
    if (!node) {
      return;
    }
    if (!data) {
      clearState(node);
      return;
    }
    node.data = data;
    if (clearValue) {
      node.value = null;
    }
    var result = undefined;
    if (data && data.incomplete) {
      clearState(node);
      result = true;
    } else {
      createOptions(node.field, data.regions, node.value);
      result = initState(node.next, data.info[node.value]);
    }
    return (result == undefined) ? checkSpecify(node, data) : result;
  }

  function updateState(node) {
    if (!node) {
      return;
    }
    node.value = node.field.val();
    var data = node.data;
    var result = initState(node.next, data.info[node.value], true);
    return (result == undefined) ? checkSpecify(node, data) : result;
  }

  function clearState(node) {
    if (!node) {
      return;
    }
    node.data = null;
    node.value = null;
    node.field.hide().empty();
    clearState(node.next);
  }

  function updateSpecify(field, visible, keeping) {
    if (!keeping) {
      field.val("");
    }
    if (visible) {
      field.show();
    } else {
      field.hide();
    }
  }

  var name = "location";
  var id = `id_${name}`;
  var countryField = $(`#${id}_0`);
  var provinceField = $(`#${id}_1`);
  var cityField = $(`#${id}_2`);
  var specifyField = $(`#${id}_3`);
  var countryValue = countryField.val();
  var provinceValue = provinceField.val();
  var cityValue = cityField.val();
  countryField.replaceWith(`<select name="${name}_0" class="form-control" title id="${id}_0"></select>`);
  provinceField.replaceWith(`<select name="${name}_1" class="form-control" title id="${id}_1"></select>`);
  cityField.replaceWith(`<select name="${name}_2" class="form-control" title id="${id}_2"></select>`);
  specifyField.attr("placeholder", "请将所在地区补充完整，一般精确到城市。");
  countryField = $(`#${id}_0`);
  provinceField = $(`#${id}_1`);
  cityField = $(`#${id}_2`);
  var cityNode = {
    field: cityField,
    value: cityValue,
    data: null,
    next: null
  };
  var provinceNode = {
    field: provinceField,
    value: provinceValue,
    data: null,
    next: cityNode
  };
  var countryNode = {
    field: countryField,
    value: countryValue,
    data: null,
    next: provinceNode
  };

  countryField.change(function() {
    var displaySpecify = updateState(countryNode);
    updateSpecify(specifyField, displaySpecify);
  });
  provinceField.change(function() {
    var displaySpecify = updateState(provinceNode);
    updateSpecify(specifyField, displaySpecify);
  });
  cityField.change(function() {
    var displaySpecify = updateState(cityNode);
    updateSpecify(specifyField, displaySpecify);
  });
  var displaySpecify = initState(countryNode, locationData);
  updateSpecify(specifyField, displaySpecify, true);
});
