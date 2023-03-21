$(document).ready(function () {
    $("#test-data-form").on("submit", function (event) {
        event.preventDefault();

        let selectedScript = $("input[name='script']:checked").val();
        let numFiles = $("#num_files").val();

        $.ajax({
            url: "/generate_test_data",
            method: "POST",
            data: {
                script: selectedScript,
                num_files: numFiles
            },
            success: function (response) {
                console.log('status:', response.status); // Log status property
                console.log('download_url:', response.download_url); // Log download_url property
                if (response.status === "success") {
                    // Create a hidden anchor element and use it to download the file
                    let hiddenAnchor = $('<a>', {
                        href: response.download_url,
                        download: '',
                        style: 'display:none'
                    }).appendTo('body');
                    hiddenAnchor[0].click();
                    hiddenAnchor.remove();
                } else {
                    alert("Error generating test data. Please try again.");
                }
            },
            error: function () {
                alert("Error generating test data. Please try again.");
            }
        });
    });
});

function updateNumFilesLabel(value) {
    $("#num_files_label").text(value);
}