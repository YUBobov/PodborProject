//иницилизируем пространство имен для доступа к компонентам карты
ymaps.ready(init); 



function init() {
	//конструктор
	let map = new ymaps.Map('map', {
		center: [56.84, 60.61], // центр карты
		zoom: 15
	});
	//
	map.controls.add('zoomControl');
	//
	//map.controls.add('searchControl');
	//Для измерения расстояния
	map.controls.add('mapTools');
	map.controls.add('searchControl');
	var button1 = document.getElementById("btn");
	button1.onclick = dist;
	//Функция подсчета расстояния карта
	function dist () {
	    console.log(map.behaviors.get('ruler').geometry.getCoordinates());
	    line = map.behaviors.get('ruler').geometry.getCoordinates();
	    console.log(line.length);
	    dista = 0;
	    for (let i = 0; i < line.length-1; i++) {
	    		dista += ymaps.coordSystem.geo.getDistance(line[i],line[i+1]);
	    		console.log(dista);
}
	
}
}


/*route.model.events.add('requestsuccess', function () {

            var activeRoute = route.getActiveRoute();
            if (activeRoute) {
                // Получим протяженность маршрута.
                var length = route.getActiveRoute().properties.get("distance")
                print(length.value)
            }
        });*/
//print(Map.baloon.getData.value())  





