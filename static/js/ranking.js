import * as React from 'react';
import { DataGrid } from '@material-ui/data-grid';


/**
 * sends a request to the specified url from a form. this will change the window location.
 * @param {string} path the path to send the post request to
 * @param {object} params the paramiters to add to the url
 * @param {string} [method=post] the method to use on the form
 */

const columns = [
  { field: 'id', headerName: 'Pozycja', width: 130 },
  { field: 'username', headerName: 'Użytkownik', width: 130 },
  { field: 'points', headerName: 'Punkty', width: 130 },
];

function post(path, params, method='post') {

  // The rest of this code assumes you are not using a library.
  // It can be made less wordy if you use one.
  const form = document.createElement('form');
  form.method = method;
  form.action = path;

  for (const key in params) {
    if (params.hasOwnProperty(key)) {
      const hiddenField = document.createElement('input');
      hiddenField.type = 'hidden';
      hiddenField.name = key;
      hiddenField.value = params[key];

      form.appendChild(hiddenField);
    }
  }

  document.body.appendChild(form);
  form.submit();
}

const SelectAction = [  
  {
    icon: "glyphicon glyphicon-link",
    actions: [      
      {
        text: "Pokaż typy",
        callback: () => {
          console.log("SELECTED");
          alert("Option 2 clicked");
        }
      }
    ]
  }
];
function getCellActions(column, row) {
  const cellActions = {
    username: SelectAction
  };
  return row.id % 2 === 0 ? cellActions[column.key] : null;
}





  

export default function DataTable() {
  return (
    <div style={{ height: 400, width: 500 }}>
      <DataGrid rows={rows} columns={columns} pageSize={5} getCellActions={getCellActions} disableMultipleSelection={true}  />
    </div>
  );
}