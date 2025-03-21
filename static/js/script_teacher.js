/*
! Created On Thu January 02 11:15 PM 2025

! @author: Talha Usman
! Status: Developer
*/

function exportTableToExcel() {
  // Get the original table
  const originalTable = document.getElementById("resultsTable");

  // Create a temporary table element
  const tempTable = document.createElement("table");
  tempTable.innerHTML = originalTable.innerHTML;

  // Convert the temporary table to a workbook
  const workbook = XLSX.utils.table_to_book(tempTable, { sheet: "Results" });

  // Export the workbook to an Excel file
  XLSX.writeFile(workbook, "results.xlsx");
}
