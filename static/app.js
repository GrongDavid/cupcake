const BASE_URL = 'http://127.0.0.1:5000/api/cupcakes'

function cupcakeHTML(cupcake) {
    return `
      <div data-cupcake-id=${cupcake.id}>
        <li>
          Flavor: ${cupcake.flavor} / Size: ${cupcake.size} / Rating: ${cupcake.rating}
          <button class="delete-button">X</button>
        </li>
        <img class="Cupcake-img"
              src="${cupcake.image}"
              alt="(no image provided)">
      </div>`;
  }

async function listAllCupcakes(){
    const response = await axios.get(BASE_URL);
    const allCupcakes = response['data']['cupcakes'];
    
    allCupcakes.forEach(cupcake => {
        let newCupcake = cupcakeHTML(cupcake);
        $('#cupcakes-list').append(newCupcake);
    })
    console.log(response);
    console.log(allCupcakes);
}

$("#cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();
  
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();
    if(image == ''){
        image = null;
    }
    console.log(image);
  
    const cupcakeResponse = await axios.post(`${BASE_URL}`, data= {
      flavor,
      rating,
      size,
      image
    });
  
    let newCupcake = $(cupcakeHTML(cupcakeResponse.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#cupcake-form").trigger("reset");
  });

  $("#cupcakes-list").on("click", ".delete-button", async function (evt) {
    evt.preventDefault();
    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");
  
    await axios.delete(`${BASE_URL}/${cupcakeId}`);
    $cupcake.remove();
  });
  

listAllCupcakes();