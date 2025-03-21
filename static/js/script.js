/*
! Created On Thu January 02 11:11 PM 2025

! @author: Talha Usman
! Status: Developer
*/

function exportTableToExcel() {
  // Get the original table
  const originalTable = document.getElementById("resultsTable");

  // Create a temporary table element
  const tempTable = document.createElement("table");
  tempTable.innerHTML = originalTable.innerHTML;

  // Remove the last column (Actions) from the header
  tempTable
    .querySelectorAll("thead tr th:last-child")
    .forEach((th) => th.remove());

  // Remove the last column (Actions) from all rows in the body
  tempTable.querySelectorAll("tbody tr").forEach((row) => {
    row.querySelectorAll("td:last-child").forEach((td) => td.remove());
  });

  // Convert the temporary table to a workbook
  const workbook = XLSX.utils.table_to_book(tempTable, { sheet: "Results" });

  // Export the workbook to an Excel file
  XLSX.writeFile(workbook, "results.xlsx");
}
