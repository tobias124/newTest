function showHideElement(id){
    var x = document.getElementById(id);
    if (x.style.display === 'none')
    {
      x.style.display = 'block';
    } else
    {
      x.style.display = 'none';
    }
  }

    function filterTable(table_id, inputfield_id) {
      var input, filter, table, tr, td, i, txtValue;
      input = document.getElementById(inputfield_id);
      filter = input.value.toUpperCase();
      table = document.getElementById(table_id);
      tr = table.getElementsByTagName("tr");
      for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
          txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
          } else {
            if(tr[i].id != "xx") tr[i].style.display = "none";
          }
        }       
      }
    }
