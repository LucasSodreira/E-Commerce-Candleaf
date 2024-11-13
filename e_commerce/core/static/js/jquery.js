$(document).ready(function () {
  $("#filtro-form").submit(function (e) {
      e.preventDefault();

      var nomeProduto = $("#input-filter").val();
      var categoriaId = $("#filter").val();  // Corrigido para 'categoriaId'

      $.ajax({
          url: '{% url "index" %}',
          method: "GET",
          data: {
              nome_produto: nomeProduto,
              categoria: categoriaId,  // Corrigido para 'categoria'
          },
          success: function (data) {
              $(".container-products").html(data);
          },
          error: function (error) {
              console.log("Erro ao enviar a requisição de filtro:", error);
          },
      });

      return false;
  });
});
