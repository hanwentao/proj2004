$(function() {
  var locationData = {
    regions: ['中国', '美国'],
    info: {
      '中国': {
        regions: ['北京', '浙江'],
        info: {
          '浙江': {
            regions: ['杭州', '宁波']
          }
        }
      }
    }
  };

  var updateOptions = function(field, data, selected) {
    field.empty();
    if (data === undefined) {
      field.attr("disabled", "disabled");
      return;
    }
    field.removeAttr("disabled");
    field.append("<option value>---------</option>");
    var options = data.regions;
    for (var option of options) {
      var option_element = $(`<option value="${option}">${option}</option>`).appendTo(field);
      if (option == selected) {
        option_element.attr("selected", "selected");
      }
    }
  };

  var countryField = $("#id_location_0");
  var provinceField = $("#id_location_1");
  var cityField = $("#id_location_2");
  var selectedCountry = countryField.val();
  var selectedProvince = provinceField.val();
  var selectedCity = cityField.val();
  countryField.replaceWith(`<select name="location_0" class="form-control" title id="id_location_0"></select>`);
  provinceField.replaceWith(`<select name="location_1" class="form-control" title id="id_location_1"></select>`);
  cityField.replaceWith(`<select name="location_2" class="form-control" title id="id_location_2"></select>`);

  countryField = $("#id_location_0");
  provinceField = $("#id_location_1");
  cityField = $("#id_location_2");
  updateOptions(countryField, locationData, selectedCountry);
  updateOptions(provinceField, locationData.info[selectedCountry], selectedProvince);
  if (locationData.info[selectedCountry] !== undefined) {
    updateOptions(cityField, locationData.info[selectedCountry].info[selectedProvince], selectedCity);
  } else {
    updateOptions(cityField);
  }

  countryField.change(function() {
    var selectedCountry = $(this).val();
    var provinceField = $("#id_location_1");
    var cityField = $("#id_location_2");
    updateOptions(provinceField, locationData.info[selectedCountry]);
    updateOptions(cityField);
  });
  provinceField.change(function() {
    var selectedCountry = $("#id_location_0").val();
    var selectedProvince = $(this).val();
    var cityField = $("#id_location_2");
    updateOptions(cityField, locationData.info[selectedCountry].info[selectedProvince]);
  });
});
