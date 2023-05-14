// // 添加按钮事件
// // 获取查看/修改按钮
// const editBtn = document.getElementById("edit-btn");

// // 监听添加按钮点击事件
// editBtn.addEventListener("click", function() {
//     // 跳转到添加页面
//     window.location.href = "/tactic/tactic_edit/";
// });

$(document).ready(function () {

	// 更新按钮点击事件
    $(".update-btn").click(function () {
      window.location.reload(); // 重新加载页面
    });


    // 查看/修改按钮点击事件
    $(".edit-btn").click(function () {

        // 获取当前的按钮对应的 data-id 值
        var tactic_id = $(this).attr("data-id");
        $('#id-input').val(tactic_id);
        $('#edit-form').submit();
    });


    // 删除按钮点击事件
    $(".delete-btn").click(function (event) {
    	// 取消表单提交默认行为
        event.preventDefault();

        var tactic_id = $('input[name="tactic_select"]:checked').val();

        if (!tactic_id) {
            alert('请先选择需要删除策略');
            return;
        }

        // 弹出确认删除提示框
        $('#confirm-delete-modal').modal('show');

        $('#confirm-delete-btn').click(function() {
        	// 隐藏确认删除提示框
            $('#confirm-delete-modal').modal('hide');

            $.ajax({
                url: $('#delete-form').attr('action'),
                method: "post",
                data: {
                    csrfmiddlewaretoken: "{{ csrf_token }}",
                    tactic_id: tactic_id,
                },
                success: function (response) {
                    // 显示删除成功提示
                    alert('删除成功');
                    
                    // 删除后重载页面
                    window.location.reload();
                },
                error: function(response) {
                    // 删除失败，输出错误信息
                    alert('删除失败：' + response.error);
                }
            });
        });
    });

})