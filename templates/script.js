$(document).ready(function() {

  // *** UPLOAD ELEMENT FUNCTION ***
  // FOR: add-element.html
  // Send form containing element data to 
  // do_POST: '/upload-element'
  $('#upload-element').submit(function(event) {
     //event.preventDefault();
     let formData = new FormData(this)
     console.log(formData)


    $.ajax({
      url: '/upload-element',
      type: 'POST',
      data: formData,
      success: function(response) {
        // $('#output').html(response);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log(textStatus, errorThrown);
      }
    });
  });
  // *** END OF FUNCTION ***


  // *** DELETE ELEMENT FUNCTION ***
  // FOR: delete-element.html
  // After clicking an entry, confirm if the user wants to 
  // delete that element. If yes, send the name of the element
  // to do_POST: '/delete-element' for it to be deleted
  const elementEntries = $(".element-entry");

  const elementEntryPressed = e => {
    let name = $(e.target).parent().attr("name");
    console.log(e.target);  // Get ID of Clicked Element
    let result = confirm(`Delete Element ${name}?`);
    if (result  == true ) {

      $.ajax({
        type: "POST",
        url: "/delete-element",
        data: name,

        success: function(response) {
          // Request successful, do something with response
          console.log(response);
        },
        error: function(xhr, status, error) {
          // Request failed, handle error
          console.log(error);
        }

      });
      alert(`Element ${name} successfully deleted`);
      window.location.replace('/remove-element.html');

    }
  }

  // add event listener for each row in the table
  for (let entry of elementEntries) {
    entry.addEventListener("click", elementEntryPressed);
  }

  // *** END OF FUNCTION ***

  // *** VIEW MOLECULE FUNCTION ***
  // FOR: view-molecule.html
  // After clicking an entry, confirm if the user wants to 
  // view that molecule. If yes, send the name of the molecule
  // to do_POST: '/display-molecule' for it to be deleted
  const moleculeEntries = $(".molecule-entry");

  const moleculeEntryPressed = e => {
    let name = $(e.target).parent().attr("name");
    let result = confirm(`Display Molecule ${name}?`);
    if (result  == true ) {


      $.ajax({
        type: "POST",
        url: "/display-molecule",
        data: name,

        success: function(response) {
          // Request successful, do something with response
          console.log(response);
        },
        error: function(xhr, status, error) {
          // Request failed, handle error
          console.log(error);
        }

      });

    }
  }

  // add event listener for each row in the table
  for (let entry of moleculeEntries) {

    entry.addEventListener("click", moleculeEntryPressed);
  }

});

(function () {
  let old = console.log;
  let logger = document.getElementById('log');
  console.log = function (message) {
      if (typeof message == 'string') {

        if (message.includes("<!DOCTYPE html>"))
          document.documentElement.innerHTML = message;
      }
  }
})();