const Q = require('q');
const child_process = require('child_process');
const path = require('path');
module.exports = (script, payload) => {
	let stdout = "", stderr = "";
	let child = child_process.spawn('python', [script]),
		deferred = Q.defer();
	child.stdout.on('data', (data) => {
		stdout += JSON.parse(data.toString());
	});
	child.stderr.on('data', (err) => {
		stderr += err.toString();
	});
	child.on('close', (code, signal) => {
		if(code !== 0 || !JSON.parse(stdout).success)
			deferred.reject(stderr);
		else
			deferred.resolve(uuid);
	})
	child.stdin.setEncoding('utf-8');
	child.stdin.write(JSON.stringify(payload)); //passing to stdin
	child.stdin.write('\u0004\n');
	return deferred.promise;
}