var Tools = Tools || {};

Tools.Send = function(msg){
    // Send message to MenuBar_Listner.Action
    // the action must be an existing python function.
    // this will be evaluate by 
    document.title = "_";
    document.title = msg;

}
Tools.Create_root_container = function(){
    root_container = document.createElement('div');
    root_container.id = "root_container";
    root_container.className = "root_container";
    root_container.style.width = "10000px";
    //root_container.style.height = height;
    root_container.style.overflow = "hidden";
    document.body.appendChild(root_container);
    return true   

}
Tools.Create_stage = function(width, height, id, zindex, classname){
    console.log(classname);
    
    new_stage = document.createElement('div');
    new_stage.id = id;
    new_stage.className = String(classname);
    new_stage.style.width = width;
    new_stage.style.height = height;
    new_stage.style.position = "relative";
    new_stage.style.zIndex = zindex;
    //new_stage.style.left = "500px";
    root_container = document.getElementById('root_container')
    root_container.appendChild(new_stage);
    return true   

}
Tools.slide_stage = function(stage_id, speed, direction, position){

    if(direction === "1"){$("#" + stage_id).animate({"left": position}, 300);};
    if(direction === "2"){$("#" + stage_id).animate({"right": position}, 300);};
       
}

Tools.Create_Button = function(action_name, text, classname, destination_id){
    new_button = document.createElement('div');
    new_button.className = classname;
    new_button.innerText = text;
    new_button.onclick = function(){
        Tools.Send(action_name);
    }
    stage = document.getElementById(destination_id)
    stage.appendChild(new_button);
    return true   
}

Tools.Create_Button_Fixed = function(action_name, text, classname, destination_id){
    new_button = document.createElement('div');
    new_button.className = classname;
    new_button.innerText = text;
    new_button.style.position = "absolute";
    new_button.style.zIndex = "1000";
    new_button.onclick = function(){
        Tools.Send(action_name);
    }
    stage = document.getElementById(destination_id)
    stage.appendChild(new_button);
    return true   
}


