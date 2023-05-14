$(document).ready(function() {

    // 获取 ID 为 "node-status" 的输入框元素对象
    var nodeStatus = $("#node-status");
    var flag = (nodeStatus.attr("placeholder") == "offline")
    
    if (flag) {
      $("#online-id").click(function(event) {
          // 阻止默认行为
          event.preventDefault();

          // 设备离线，弹出提示信息
          alert("设备离线，无法在线导出配置文件");
          $("#online-id").prop("disabled", true);
      });
    }


    // 获取按钮事件
    $("#submit_btn").click(function() {
      // 获取选择的导出方式
      var selectedRadio = $("input[name='export-radio']:checked").val();

      // device 的 id 值
       var deviceId = $('#device_id').val();

      // 定义要提交的表单数据变量
      var formData;

      // 根据导出方式组装表单数据
      if (selectedRadio == "online") {
        // 获取第一个表单中各个字段的值
        var hostname = $("#hostname").val();
        var username = $("#username").val();
        var password = $("#password").val();
        
        // 组装表单数据
        formData = {
          'hostname': hostname,
          'username': username,
          'password': password,
          'radioType': selectedRadio,
          'device_id': deviceId
        };
        
        // 提交第一个表单
        $.ajax({
          url: $("#export1").attr("action"),
          method: "POST",
          data: formData,
          success: function() {
            // 成功提交后的处理逻辑
            alert("在线导出成功！");
          },
          error: function() {
            // 失败后的处理逻辑
            alert("在线导出失败！");
          }
        });
      } else if (selectedRadio == "offline") {
       
        // 获取文件域中选中的文件
        var configFile = $("#config-file")[0].files[0];
        
        if (!configFile) {  // 判断文件是否为空
          alert("请选择要导入的配置文件！");
          return;
        }
        
        // 创建表单对象
        formData = new FormData();
        // 将选中的文件添加到表单对象中
        formData.append("config-file", configFile);
        formData.append("radioType", selectedRadio);
        formData.append("device_id", deviceId);
        
        // 提交第二个表单
        $.ajax({
          url: $("#export2").attr("action"),
          method: "POST",
          data: formData,
          processData: false,
          contentType: false,
          success: function() {
            // 成功提交后的处理逻辑
            alert("手动导入成功！");
          },
          error: function() {
            // 失败后的处理逻辑
            alert("手动导入失败！");
          }
        });
      }
    });

});
