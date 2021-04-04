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
    let tableIngredients = document.getElementById("table-ingredients");
    let newIngredient = tableIngredients.insertRow(-1);
    newIngredient.innerHTML =
      '<tr><td><input type="text" class="form-control" placeholder="250gr flour"></td><td><button type="button" class="btn btn-secondary" onclick="removeRow($(this))">Remove</button></td></tr>';
  });
  $("#button-steps").click(function () {
    let tableSteps = document.getElementById("table-steps");
    let newStep = tableSteps.insertRow(-1);
    newStep.innerHTML =
      '<tr><td><input type="text" class="form-control" placeholder="Mix flour and water until they thicken"></td><td><button type="button" class="btn btn-secondary" onclick="removeRow($(this))">Remove</button></td></tr>';
  });

  // Finally, submit handler
  $("#button-submit").click(submit);
});

function removeRow(button) {
  // Only remove row if there are more than one row
  if (button.closest("table").prop("rows").length > 1) {
    button.closest("tr").remove();
  }
}

function submit() {
  let formData = new FormData(document.getElementById("create-form"));
  let data = Object.fromEntries(formData.entries());
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
  fetch("/recipe/create", {
    method: "POST",
    body: JSON.stringify(data),
  }).catch((error) => console.log(error));
}
