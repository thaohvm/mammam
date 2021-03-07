document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("button-ingredients").onclick = add_ingredient;
    document.getElementById("button-steps").onclick = add_step;
});

function add_ingredient() {
    let tableIngredients = document.getElementById("table-ingredients");
    let newIngredient = tableIngredients.insertRow(-1);
    newIngredient.innerHTML = '<tr><td><input type="text" class="form-control" placeholder="250gr flour"></td><td><button type="button" class="btn btn-secondary" onclick="remove_row($(this))">Remove</button></td></tr>';
}

function add_step() {
    let tableSteps = document.getElementById("table-steps");
    let newStep = tableSteps.insertRow(-1);
    newStep.innerHTML = '<tr><td><input id="first-step" type="text" class="form-control" placeholder="Mix flour and water until they thicken"></td><td><button type="button" class="btn btn-secondary" onclick="remove_row($(this))">Remove</button></td></tr>';
}

function remove_row(button) {
    // Only remove row if there are more than one row
    if (button.closest("table").prop("rows").length > 1) {
        button.closest("tr").remove();
    }
}