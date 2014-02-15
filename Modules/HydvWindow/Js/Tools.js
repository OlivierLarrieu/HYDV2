var Tools = Tools || {};

Tools.Send = function(msg){
    // Send message to MenuBar_Listner.Action
    // the action must be an existing python function.
    // this will be evaluate by 
    document.title = "_";
    document.title = msg;
}
Tools.Create_root_container = function(width, height){
    Tools.container = document.createElement('div');
    Tools.container.style.width = width;
    Tools.container.style.height = height;
    Tools.container.style.overflow = "hidden";
    Tools.container.className = "container";
    root_container = document.createElement('div');
    root_container.id = "root_container";
    root_container.style.width = "10000";
    root_container.style.minHeight = height;
    root_container.style.overflow = "hidden";
    root_container.className = "root_container";
    Tools.container.appendChild(root_container);
    document.body.appendChild(Tools.container);
    return true   

}
Tools.Create_Header = function(){
    Tools.Header = document.createElement('div');
    Tools.Header.id = "header";
    Tools.Header.style.minWidth = "100%";
    Tools.Header.style.minHeight = "25px";
    Tools.Header.style.position = "fixed";
    Tools.Header.style.top = "0px";
    Tools.Header.style.left = "0px";
    Tools.Header.style.zIndex = "10000";
    Tools.Header.className = "header";
    Tools.container.appendChild(Tools.Header);
}
Tools.Header_add = function(element_id){
    element = document.getElementById(element_id);
    element.style.visibility = "visible";
    Tools.Header.appendChild(element);
}

Tools.Create_Footer = function(){
    Tools.Footer = document.createElement('div');
    Tools.Footer.id = "header";
    Tools.Footer.style.minWidth = "100%";
    Tools.Footer.style.minHeight = "35px";
    Tools.Footer.style.position = "fixed";
    Tools.Footer.style.bottom = "0px";
    Tools.Footer.style.left = "0px";
    Tools.Footer.style.zIndex = "10000";
    Tools.Footer.className = "footer";
    Tools.container.appendChild(Tools.Footer);
}
Tools.Footer_add = function(element_id){
    element = document.getElementById(element_id);
    element.style.visibility = "visible";
    Tools.Footer.appendChild(element);
}
Tools.Create_MasterStage = function(width, height, id, zindex, classname){    
    new_stage = document.createElement('div');
    new_stage.id = id;
    new_stage.style.minWidth = width;
    new_stage.style.minHeight = height+"px";
    new_stage.style.maxWidth = width;
    new_stage.style.maxHeight = height+"px";
    try{
        new_stage.style.top = Tools.Header.style.minHeight;
    }
    catch(e){
    
    }
    new_stage.style.position = "absolute";
    new_stage.style.zIndex = zindex;
    new_stage.style.left = -width+"px";
    new_stage.style.top = Tools.Header.style.minHeight+"px";
    new_stage.style.overflow = "auto";
    new_stage.style.overflowX = "hidden"
    new_stage.style.overflowY = "hidden"
    root_container = document.getElementById('root_container')
    root_container.appendChild(new_stage);
    return true   

}

Tools.Create_stage = function(width, height, id, zindex, classname){ 
    new_stage = document.createElement('div');
    new_stage.id = id;
    new_stage.style.minWidth = width;
    new_stage.style.minHeight = height;
    new_stage.style.maxWidth = width;
    new_stage.style.maxHeight = height;
    try{
        new_stage.style.top = Tools.Header.style.minHeight;
    }
    catch(e){
    
    }
    new_stage.style.position = "relative";
    new_stage.style.zIndex = zindex;
    new_stage.style.overflow = "auto";
    new_stage.style.overflowX = "hidden"
    new_stage.className = String(classname);
    root_container = document.getElementById('root_container')
    root_container.appendChild(new_stage);
    return true   

}
Tools.Create_Div = function(text, width, height, id, classname){
    Div = document.createElement('div');
    Div.style.width = width;
    Div.style.height = height;
    Div.style.float = "left";
    Div.style.fontSize = "10px";
    Div.id = id
    Div.innerText = text;
    Div.className = String(classname);
    document.body.appendChild(Div);
    return true   

}
Tools.Div_add = function(div_id, element_id){
    element = document.getElementById(element_id);
    div = document.getElementById(div_id);
    div.appendChild(element);
    element.style.visibility = "visible";

}
Tools.slide_stage = function(stage_id, speed, direction, position){
    if(direction === "1"){$("#" + stage_id).animate({"left": position}, 150);};
    if(direction === "2"){$("#" + stage_id).animate({"right": position}, 150);};
       
}

// width, height, number, zindex, classname):
Tools.Create_Button = function(text, width, height, id, classname){
    new_button = document.createElement('div');
    new_button.style.width = width+"px";
    new_button.style.height = height+"px";
    new_button.style.visibility = "hidden";
    new_button.innerText = text;
    new_button.id = id;
    new_button.className = classname;
    document.body.appendChild(new_button);
    return true   
}
Tools.Button_add = function(button_id, element_id){
    element = document.getElementById(element_id);
    button = document.getElementById(button_id);
    button.appendChild(element);
    element.style.visibility = "visible";

}

Tools.Connect_Onclick = function(action, id){
    button = document.getElementById(id);
    button.onclick = function(){
        Tools.Send(action);
    }

}
Tools.Connect_Onmouseover = function(action, id){
    button = document.getElementById(id);
    button.onmouseover = function(){
        Tools.Send(action);
    }
}
Tools.Connect_Onmouseout = function(action, id){
    button = document.getElementById(id);
    button.onmouseout = function(){
        Tools.Send(action);
    }
}

Tools.Stage_add = function(stage_id, element_id){
    element = document.getElementById(element_id);
    stage = document.getElementById(stage_id);
    stage.appendChild(element);
    element.style.visibility = "visible";
}
Tools.Create_Button_Fixed = function(action_name, text, classname, destination_id){
    new_button = document.createElement('div');
    new_button.innerText = text;
    new_button.style.position = "absolute";
    new_button.style.zIndex = "1000";
    new_button.onclick = function(){
        Tools.Send(action_name);
    }
    new_button.className = classname;
    stage = document.getElementById(destination_id)
    stage.appendChild(new_button);
    return true   
}

Tools.Create_Icon = function(width, height, id, path, classname){
    new_icon = document.createElement('img');
    new_icon.style.width = width+"px";
    new_icon.style.height = height+"px";
    new_icon.style.margin = "0px";
    new_icon.style.top = "0px";
    new_icon.style.left = "0px";
    new_icon.style.float = "left";
    new_icon.style.position = "relative";
    new_icon.style.visibility = "hidden";
    new_icon.src = path;
    new_icon.id = id;
    new_icon.className = classname;
    document.body.appendChild(new_icon);
    return true   
}

Tools.Create_ProgressBar = function(width, height, id){
    new_bar = document.createElement('div');
    new_bar.style.width = width+"px";
    new_bar.style.height = height+"px";
    new_bar.style.visibility = "hidden";
    progress = document.createElement('meter');
    progress.style.width = width+"px";
    progress.value = 50;
    progress.min = 0;
    progress.max = 100;
    new_bar.id = id;
    new_bar.className = "progressbar";
    new_bar.appendChild(progress);
    document.body.appendChild(new_bar);
    return true   
}


