document$.subscribe(function () {
  var tables = document.querySelectorAll(
    "article .catalog-summary-table table"
  );
  tables.forEach(function (table) {
    if (table.dataset.catalogTablesortInit === "1") {
      return;
    }
    table.dataset.catalogTablesortInit = "1";
    new Tablesort(table);
  });
});
