var express = require('express'),
	path	= require('path'),
	util	= require('./util.js');

var server = express().listen(5000, function() {
	console.log('[Hackathon Time] Listening on port 5000');
});

var io = require('socket.io').listen(server);

function Room(owner, code) {
	this.owner = owner;
	this.code = code;
	this.people = [];
};

Room.prototype.broadcast = function(name, data) {
	for (var i = 0; i < this.people.length; i++) {
		var person = this.people[i];

		if (io.sockets.connected[person.id]) {
			console.log("Sent to " + person.id);
			io.sockets.connected[person.id].emit(name, data);
		}
	}
};

Room.prototype.find = function(id) {
	for (var i = 0; i < this.people.length; i++) {
		var person = this.people[i];

		if (person.id == id) {
			return person;
		}
	}
};

Room.prototype.self_destruct = function() {
	for (var i = 0; i < this.people.length; i++) {
		var person = this.people[i];

		if (io.sockets.connected[person.id]) {
			io.sockets.connected[person.id].disconnect();
		}
	}
};

function Person(name, id) {
	this.name = name;
	this.id = id;
};

Person.prototype.update = function(longitude, latitude) {
	this.longitude = longitude;
	this.latitude = latitude;
};

var rooms = {};
var assigned = {};

io.sockets.on('connection', function(socket) {
	var id = socket.id;
	console.log('>>> [SOCKET.IO] ' + id + ' connected.');

	socket.on('room_created', function(data) {
		if (!data.name) {
			socket.emit('response', {error: "Invalid name!"});
			return;
		}

		rooms[id] = new Room(id, util.randrange(20000, 99999));
		rooms[id].people.push(new Person(data.name, id));
		assigned[id] = id;
		console.log('>>> [SOCKET.IO] Room created by ' + id + ' with code ' + rooms[id].code + '!');
		socket.emit('response', {data: {code: rooms[id].code}});
	});

	socket.on('room_joined', function(data) {
		if (!data.name) {
			socket.emit('response', {error: "Invalid name!"});
			return;
		}

		if (!data.code) {
			socket.emit('response', {error: "Invalid code!"});
			return;
		}

		for (var key in rooms) {
			if (rooms[key].code == data.code) {
				var room = rooms[key];
				var person = new Person(data.name, id);
				room.broadcast('room_joined', {data: {person: person}});
				assigned[id] = key;
				console.log('>>> [SOCKET.IO] ' + id + ' has joined room ' + key + '!');
				socket.emit('response', {data: {code: room.code, people: room.people}});
				room.people.push(person);
				return;
			}
		}

		socket.emit('response', {error: "Invalid code!"});
	});

	socket.on('position', function(data) {
		console.log(">>> [SOCKET.IO] Received position from " + id + "!");

		if (rooms[assigned[id]]) {
			var room = rooms[assigned[id]];
			var person = room.find(id);

			if (person) {
				person.update(data.longitude, data.latitude);
				room.broadcast('position', {data: {person: person}});
			}
		}
	});

	socket.on('image_change', function(data) {
		console.log(">>> [SOCKET.IO] Received image_change from " + id + "!");

		if (rooms[assigned[id]]) {
			var room = rooms[assigned[id]];
			var person = room.find(id);

			if (person) {
				person.image = data.base64;
				room.broadcast("image_change", {data: {person: person}});
			}
		}
	});

	socket.on('disconnect', function() {
		console.log('>>> [SOCKET.IO] ' + id + ' disconnected!');
		var room = rooms[assigned[id]];
		delete assigned[id];

		if (room) {
			room.people.splice(room.find(id), 1);

			if (room.owner == id) {
				console.log('>>> [SOCKET.IO] Room ' + room.owner + ' has been terminated.')
				room.broadcast('response', {error: "Room creator has left the room, room deleted."});
				room.self_destruct();
				delete rooms[id];
			}
		}
	});
});








