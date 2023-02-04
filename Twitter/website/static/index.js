function deleteNote(lista) {
  noteId = lista[1];
  fetch('/delete-note', {
    method: 'POST',
    body: JSON.stringify({ noteId: noteId}),
  }).then((_res) => {
    s = "/note/" + lista[0];
    window.location.href = s;
  });
}

function search(buttonID) {
  if(event.keyCode == 13) {
      document.getElementById(buttonID).click();
  }
}

function gotoUser(buttonID) {
  document.getElementById(buttonID).click();
}

function textAreaAdjust(element) {
  element.style.height = "1px";
  if (element.clientHeight <= 40) {
    if (element.scrollHeight > element.clientHeight) {
      element.style.height = 50 + "px";
    }
  }
}