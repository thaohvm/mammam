document.addEventListener("DOMContentLoaded", function () {
  // Update image file name whenever selected
  let defaultImageLabel = $("#recipe-image-label").text();
  $("#recipe-image").change(function () {
    if ($(this).get(0).files.length === 0) {
      $("#recipe-image-label").text(defaultImageLabel);
    } else {
      $("#recipe-image-label").text($(this).val().split("\\").pop());
    }
  });

  // Add row when clicked on ingredient or step
  $("#button-ingredients").click(function () {
    let newIngredient = $("#table-ingredients")[0].insertRow(-1);
    newIngredient.innerHTML =
      '<tr><td><input type="text" class="form-control" placeholder="250gr flour" required></td><td><button type="button" class="btn btn-secondary" onclick="removeRow($(this))">Remove</button></td></tr>';
  });
  $("#button-steps").click(function () {
    let newStep = $("#table-steps")[0].insertRow(-1);
    newStep.innerHTML =
      '<tr><td><input type="text" class="form-control" placeholder="Mix flour and water until they thicken" required></td><td><button type="button" class="btn btn-secondary" onclick="removeRow($(this))">Remove</button></td></tr>';
  });

  // Finally, main handler
  $("#button-submit").click({ update: false }, submit);
  $("#button-update").click({ update: true }, submit);
});

function removeRow(button) {
  // Only remove row if there are more than one row
  if (button.closest("table").prop("rows").length > 1) {
    button.closest("tr").remove();
  }
}

function submit(event) {
  let update = event.data.update;

  // Validate form data first and stop if there're invalid data
  if (!$("#recipe-form")[0].checkValidity()) {
    $("#recipe-form").addClass("was-validated");
    return;
  }

  let formData = new FormData($("#recipe-form")[0]);
  let data = Object.fromEntries(formData.entries());
  delete data["image"]; // Image is handled separately from JSON data

  // Parse ingredients and steps into arrays
  data["ingredients"] = $("table#table-ingredients tr")
    .map(function () {
      return $(this)
        .find("td input")
        .map(function () {
          return $(this).val();
        })
        .get();
    })
    .get();
  data["steps"] = $("table#table-steps tr")
    .map(function () {
      return $(this)
        .find("td input")
        .map(function () {
          return $(this).val();
        })
        .get();
    })
    .get();

  // Generate new FormData for POST request with image file
  let images = $("#recipe-image").prop("files");
  let postData = new FormData();
  postData.append("data", JSON.stringify(data));
  postData.append("image", images[0]);

  if (update) {
    // This is an update request
    let id = $("#recipe-title").attr("data-id");
    fetch("/recipe/" + id, {
      method: "POST",
      body: postData,
    })
      .then((response) => response.json())
      .then((result) => {
        if (result["status"] != "OK") {
          swal({
            text: "Failed to update recipe. Please try again!",
            icon: "error",
          });
        } else {
          window.location.replace(result["url"]);
        }
      })
      .catch((error) => {
        console.log("Update failed: ", error);
        swal({
          text: "Failed to update recipe. Please try again!",
          icon: "error",
        });
      });
  } else {
    // This is a creation request
    fetch("/recipe/create", {
      method: "POST",
      body: postData,
    })
      .then((response) => response.json())
      .then((result) => {
        if (result["status"] != "OK") {
          swal({
            text: "Failed to create recipe. Please try again!",
            icon: "error",
          });
        } else {
          window.location.replace(result["url"]);
        }
      })
      .catch((error) => {
        console.log("Create failed: ", error);
        swal({
          text: "Failed to create recipe. Please try again!",
          icon: "error",
        });
      });
  }
}