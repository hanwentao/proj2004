$(function() {
  $("#profile-form").submit(function(event) {
    var photo = $("#id_photo")[0];
    if (photo.files[0] && photo.files[0].size > 2097152) {
      alert("上传图片大小不能超过 2MB。");
      event.preventDefault();
    }
  });
});
