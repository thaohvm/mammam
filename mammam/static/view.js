document.addEventListener("DOMContentLoaded", function () {
  $("#button-update").click(function () {});
  $("#button-delete").click(function () {
    swal({
      title: "Are you sure?",
      text: "Once deleted, you will not be able to recover this recipe!",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    }).then((confirmed) => {
      if (confirmed) {
        let id = $("#recipe-title").attr("data-id");
        fetch("/recipe/" + id, { method: "DELETE" })
          .then((response) => response.json())
          .then((result) => {
            if (result["status"] != "OK") {
              swal({
                text: "Failed to delete the recipe. Please try again!",
                icon: "error",
              });
            } else {
              window.location.replace("/");
            }
          })
          .catch((error) => {
            console.log("Delete failed: ", error);
            swal({
              text: "Failed to delete the recipe. Please try again!",
              icon: "error",
            });
          });
      }
    });
  });
});
