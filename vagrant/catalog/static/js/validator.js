function validateAddCategoryForm() {
    let x = document.forms["addCategory"]["categoryName"].value;
    if (x == "") {
        alert("Category name field Cannot be empty");
        return false;
    }
}

function validateAddItemForm() {
    let x = document.forms["addItem"]["itemName"].value;
    if (x == "") {
        alert("Item name field Cannot be empty");
        return false;
    }
}