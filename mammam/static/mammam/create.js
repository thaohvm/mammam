document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("button-ingredients").onclick = add_ingredient;
    document.getElementById("button-steps").onclick = add_step;
});

function add_ingredient() {
    let tableIngredients = document.getElementById("table-ingredients");
    let newIngredient = tableIngredients.insertRow(-1);
    newIngredient.innerHTML = '<tr><td><input type="text" class="form-control" placeholder="250gr flour"></td></tr>';
}

function add_step() {
    let tableSteps = document.getElementById("table-steps");
    let newStep = tableSteps.insertRow(-1);
    newStep.innerHTML = '<tr><td><input type="text" class="form-control" placeholder="Mix flour and water until they thicken"></td></tr>';
}