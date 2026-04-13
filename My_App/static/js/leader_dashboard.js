
  // Filter tasks by status
  document.querySelectorAll("[data-filter]").forEach((button) => {
    button.addEventListener("click", function () {
      document
        .querySelectorAll("[data-filter]")
        .forEach((btn) => btn.classList.remove("active"));
      this.classList.add("active");

      const filter = this.getAttribute("data-filter");
      document.querySelectorAll(".task-row").forEach((row) => {

        const statusSpan = row.querySelector('[data-status_01]')
        // console.log(statusSpan.getAttribute("data-status_01"))


        // if (statusSpan) {
        // console.log(statusSpan.getAttribute('data-status_01'));
        // } else {
        // console.log('No data-status_01 found in this row');
        // }
        

        if (filter === "all" || statusSpan.getAttribute("data-status_01") === filter) {
          row.style.display = "";
          // console.log("Showing row with status:", statusSpan.getAttribute("data-status_01"));
          // console.log("Filter applied:", filter);
        } else {
          row.style.display = "none";
          // console.log("Hiding row with status:", statusSpan.getAttribute("data-status_01"));
          // console.log("Filter applied:", filter);
        }
          
      });
    });
    

  });

  // Resolve Task Modal Handling
  document
    .getElementById("resolveTaskModal")
    .addEventListener("show.bs.modal", function (event) {
      const button = event.relatedTarget;
      const taskId = button.getAttribute("data-task-id");
      const taskTitle = button.getAttribute("data-task-title");

      document.getElementById("resolve-task-id").value = taskId;
      document.getElementById("resolve-task-title").textContent = taskTitle;
    });

  // Toggle postpone section based on action selection
  document.querySelectorAll('input[name="resolveAction"]').forEach((radio) => {
    radio.addEventListener("change", function () {
      const postponeSection = document.getElementById("postpone-section");
      if (this.value === "postpone") {
        postponeSection.style.display = "block";
        document.getElementById("newDeadline").name = "newDeadline"; //********************************
        document.getElementById("newDeadline").required = true;
      } else {
        postponeSection.style.display = "none";
        document.getElementById("newDeadline").name = "newDeadline"; //********************************
        document.getElementById("newDeadline").required = false;
      }
    });
  });

  // Resolve task form submission
  document
    .getElementById("resolve-task-form")
    .addEventListener("submit", function (e) {
      e.preventDefault();

      const taskId = document.getElementById("resolve-task-id").value;
      console.log("Resolving task ID:", taskId);
      const action = document.querySelector(
        'input[name="resolveAction"]:checked',
      ).value;
      console.log("Resolving task action:", action);
      const formData = new FormData();
      formData.append("action", action);

      if (action === "postpone") {
        const newDeadline = document.getElementById("newDeadline").value;
        if (!newDeadline) {
          alert("Please select a new deadline");
          return;
        }
        formData.append("new_deadline", newDeadline);
      }

      fetch(`/task/${taskId}/resolve`, {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            bootstrap.Modal.getInstance(
              document.getElementById("resolveTaskModal"),
            ).hide();
            location.reload(); // Refresh the page to update task status
          } else {
            alert("Error: " + (data.message || "Failed to update task"));
          }
        })
        .catch((error) => {
          //  console.error('Error:', error);  ///
          alert("An error occurred while updating the task");
        });
    });

  // Task Details Modal Handling
  document
    .getElementById("taskDetailsModal")
    .addEventListener("show.bs.modal", function (event) {
      const button = event.relatedTarget;

      document.getElementById("task-details-title").textContent =
        button.getAttribute("data-task-title");
      document.getElementById("task-details-desc").textContent =
        button.getAttribute("data-task-desc");
      document.getElementById("task-details-member").textContent =
        button.getAttribute("data-task-member");
      document.getElementById("task-details-start").textContent =
        formatDateDisplay(button.getAttribute("data-task-start"));
      document.getElementById("task-details-deadline").textContent =
        formatDateDisplay(button.getAttribute("data-task-deadline"));

      // Set status with appropriate styling
      const status = button.getAttribute("data-task-status");
      const statusEl = document.getElementById("task-details-status");
      statusEl.textContent = status.charAt(0).toUpperCase() + status.slice(1);

      if (status === "completed") {
        statusEl.className = "text-success fw-bold";
      } else if (status === "delayed") {
        statusEl.className = "text-warning fw-bold";
      } else {
        statusEl.className = "text-primary fw-bold";
      }

      // Show reason if exists
      const reasonContainer = document.getElementById(
        "task-details-reason-container",
      );
      const reasonEl = document.getElementById("task-details-reason");
      const reason = button.getAttribute("data-task-reason");

      if (reason) {
        reasonContainer.style.display = "block";
        reasonEl.textContent = reason;
      } else {
        reasonContainer.style.display = "none";
      }
    });

  // Format date for display
  function formatDateDisplay(dateString) {
    if (!dateString) return "";
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  // Show overdue alert if there are overdue tasks
  document.addEventListener("DOMContentLoaded", function () {
    // Read from data attribute - no formatting issues!
    const overdueCount = parseInt(
      document.getElementById("task-data").dataset.overdueCount || "0",
      10,
    );

    const overdueSection = document.getElementById("overdue-alert-section");

    if (overdueCount > 0 && overdueSection) {
      overdueSection.style.display = "block";
    }
  });


// ******************************** Pagintion cal **********************************************


  document.addEventListener("DOMContentLoaded", function () {
    const table = document.getElementById("data-table");

    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));
    let rowsPerPage = document.getElementById("NoOfRowPage").value;
    let totalPages = Math.ceil(rows.length / rowsPerPage);
    const paginationContainer = document.getElementById("pagination");

    // Function to display rows for the current page
    function displayRows(page) {
      rows.forEach((row, index) => {
        row.style.display = "none"; // Hide all rows initially
        if (index >= (page - 1) * rowsPerPage && index < page * rowsPerPage) {
          row.style.display = ""; // Show rows for the current page
        }
      });
    }

    // Function to generate pagination buttons
    function generatePagination() {
      paginationContainer.innerHTML = ""; // Clear existing buttons

      for (let i = 1; i <= totalPages; i++) {
        const a_li = document.createElement("a");
        const Li_Element = document.createElement("li");

        a_li.setAttribute("class", "page-link");
        Li_Element.setAttribute("class", "page-item");

        a_li.textContent = i;

        a_li.addEventListener("click", () => {
          displayRows(i); // Display rows for the clicked page
          setActiveButton(i); // Update active button style
        });

        Li_Element.appendChild(a_li);
        paginationContainer.appendChild(Li_Element);
      }

      setActiveButton(1); // Set the first button as active by default
    }

    // Function to set the active button style
    function setActiveButton(activePage) {
      const buttons = paginationContainer.querySelectorAll("a");
      buttons.forEach((button, index) => {
        button.classList.toggle("active", index + 1 === activePage);
      });
    }

    const Change_NoRaw = document.getElementById("NoOfRowPage");

    Change_NoRaw.addEventListener("change", function () {
      rowsPerPage = document.getElementById("NoOfRowPage").value;
      totalPages = Math.ceil(rows.length / rowsPerPage);
      generatePagination();
      displayRows(1);
    });

    // Initialize pagination
    generatePagination();
    displayRows(1);// Display the first page by default

    // const rowsPerPage = document.getElementById('NoOfRowPage');
   
    // Check screen size
   function updateInputValue() {
      if (window.matchMedia('(max-width: 1700px)').matches) {
        // Mobile
        rowsPerPage = 100;
        
        generatePagination();
        displayRows(1);

      } else {
        
        rowsPerPage = 6;
        
        generatePagination();
        displayRows(1);
      }
    }

   
  
    updateInputValue();
    // Run on resize
    window.addEventListener('resize', updateInputValue);


  const scrollPageBtn = document.getElementById("scrollPageBtn");

    // Define Scroll_page_Fun inside the same scope
    
    function Scroll_page_Fun() {

      const pationationArea = document.getElementById("pationation_area");
      const tableView = document.getElementById("table_view");
      const icon_v01 = document.getElementById("icon_v01");
      const viewStatus = scrollPageBtn.getAttribute("data-view-status");

      if (viewStatus === "noneScroll") {
        
        pationationArea.style.display = 'none';
        tableView.style.overflowY = 'auto';    // corrected property name
        tableView.style.overflowX = 'hidden';
        tableView.style.maxHeight = '60vh';
        scrollPageBtn.removeAttribute('data-view-status');
        scrollPageBtn.setAttribute("data-view-status", "Scroll");
        icon_v01.classList.remove("bi-chevron-bar-expand");
        icon_v01.classList.add("bi-chevron-bar-contract");
        localStorage.setItem("scroll_Paging", "yes")

        rowsPerPage = 100;
        generatePagination();
        displayRows(1);

      } else {

        pationationArea.style.display = 'block';
        tableView.style.overflowY = 'hidden';   
        tableView.style.overflowX = 'hidden';
        tableView.style.maxHeight = '60vh';
        scrollPageBtn.removeAttribute('data-view-status');
        scrollPageBtn.setAttribute("data-view-status", "noneScroll");
        icon_v01.classList.remove("bi-chevron-bar-contract");
        icon_v01.classList.add("bi-chevron-bar-expand");
        localStorage.setItem("scroll_Paging", "no") 

        rowsPerPage = 6;
        generatePagination();
        displayRows(1);
      }

  }

  // Attach the click event
  if (scrollPageBtn) {
    scrollPageBtn.addEventListener('click', function (event) {
         // prevent the anchor from navigating
      Scroll_page_Fun();
    });
    }
    
    if (localStorage.getItem("scroll_Paging") === "yes") {
    
      const pationationArea = document.getElementById("pationation_area");
      const tableView = document.getElementById("table_view");
      const icon_v01 = document.getElementById("icon_v01");
      
    
        pationationArea.style.display = 'none';
        tableView.style.overflowY = 'auto';    // corrected property name
        tableView.style.overflowX = 'hidden';
        tableView.style.maxHeight = '60vh';
        scrollPageBtn.removeAttribute('data-view-status');
        scrollPageBtn.setAttribute("data-view-status", "Scroll");
        icon_v01.classList.remove("bi-chevron-bar-expand");
        icon_v01.classList.add("bi-chevron-bar-contract");
        
        rowsPerPage = 100;
        generatePagination();
        displayRows(1);
    
    } else if (localStorage.getItem("scroll_Paging") === "no") {
      
        const pationationArea = document.getElementById("pationation_area");
        const tableView = document.getElementById("table_view");
        const icon_v01 = document.getElementById("icon_v01");
      
        pationationArea.style.display = 'block';
        tableView.style.overflowY = 'hidden';   
        tableView.style.overflowX = 'hidden';
        tableView.style.maxHeight = '60vh';
        scrollPageBtn.removeAttribute('data-view-status');
        scrollPageBtn.setAttribute("data-view-status", "noneScroll");
        icon_v01.classList.remove("bi-chevron-bar-contract");
        icon_v01.classList.add("bi-chevron-bar-expand");
        localStorage.setItem("scroll_Paging", "no") 

        rowsPerPage = 6;
        generatePagination();
        displayRows(1);
    }
    
  });
 

//******************************** End Pagintion cal **********************************************

//******************************** Add event listener to the entire document  **********************
 
document.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevent default behavior
      document.getElementById('SearchBut').click(); // Trigger the button click
    }
});
  
//******************************** Search  document  **********************
function Search_Fun() {

  let Search_V = document.querySelector(".Search_But").value.trim()
  if (Search_V == "") {
    window.location.href = "/"
  } else {
    window.location.href = "/Search_Data?search_v=" + Search_V
  }
}

// ************************  for filter log by task id ***********************************



  function filterRows() {

    const hiddenInput = document.getElementById('log-task-id');
    const rows = document.querySelectorAll('#logs-tbody .task-row');
    const selectedTaskId = hiddenInput.value;

    rows.forEach(row => {
      if (!selectedTaskId || row.dataset.taskId === selectedTaskId) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
}
  
document.getElementById('taskLogModal').addEventListener('show.bs.modal', function (event) {
    console.log("Task Log Modal is being shown");
  
    const button = event.relatedTarget;
    const taskId = button.getAttribute('data-task-id');
  
    console.log(taskId)
  
    document.getElementById('log-task-id').value = taskId;
    filterRows();
  });



    