/*$(document).ready(function() {
  // Get the search input
  var searchInput = $('#search-input');

  // Listen for keyup events on the search input
  searchInput.on('keyup', function() {
    // Get the value of the search input
    var query = $(this).val();

    // Make an Ajax request to the search endpoint
    $.ajax({
      url: '/search/',
      data: {
        q: query
      },
      success: function(data) {
        // Update the results list with the search results
        $('#results-list').html(data);
      }
    });
  });
});*/

$(document).ready(function(){
                    $("#id_search_field").on('keyup', function () {
                        var query =($('#id_search_field').val());
                        //$("#event").html(query);
                        console.log(query);
                        var html_str = "";
                        $.ajax({
                            type : "GET",
                            url  : "/ajax_search/",
                            data : {
                                "query": query
                            }
                             ,
                            success : function(data)
                            {

                                const results = JSON.parse(data.results);
                                console.log(results);
                                $("#event").html("");
                                $(".disp_none").html("");
                                document.querySelector("footer").style.marginTop="20%";
                                document.querySelector(".welcome").style.marginTop="10%";
                                $('.welcome').html('Évènements Trouvé')
                                if (results.length > 0)
                                    results.forEach(function(event) {
                                        var url = "{% url 'event-detail' 0 %}"
                                        url  = url.replace("0", event.pk);
                                        var eventHTML = `
                                            <div class="event">
                                                <a href="${url}">
                                                    <img src="/media/${event.fields.image}" alt="${event.fields.name}">
                                                </a>
                                                <h3 class="name">${event.fields.name}</h3>
                                                <p class="price">${event.fields.price == 0 ? 'Gratuit' : event.fields.price + '$'}</p>
                                            </div>
                                        `;
                                        $("#event").append(eventHTML);
                                    });
                                else
                                    $('.welcome').html('Aucun Évènement Trouvé')
                            },
                            error: function(XMLHttpRequest, textStatus, errorThrown) {
                                console.log("Status: " + textStatus); //alert("Error: " + errorThrown);
                            }
                        });
                    });
                });