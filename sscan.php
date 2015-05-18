#!/usr/bin/env php
<?php
/**
 * SSH Password Scan
 *
 * @author Feei <wufeifei[at]wufeifei.com>
 * @TODO   Add Local Password Dict
 */

set_time_limit(0);
ini_set('memory_limit', '1024M');

# Config
$info = array(
	'user'     => 'root',
	'host'     => '192.168.1.1',
	'port'     => '10022',
	'password' => 'password'
);

# Usage

single($info);

#many($info);

/**
 * Detection for single target
 *
 * @param $info
 */
function single($info)
{
	if (connect($info['user'], $info['host'], $info['port'], $info['password'])) {
		error_log('[SUCCESS]' . $info['host']);
		echo '[SUCCESS]' . $info['host'] . PHP_EOL;
	} else {
		error_log('FAILD' . $info['host']);
		echo '[FAILD]' . $info['host'] . PHP_EOL;
	}
}

/**
 * Detection for many target (IP 192.168.1.1 - 192.168.1.255)
 *
 * @param $info
 */
function many($info)
{
	for ($i = 1; $i <= 255; $i++) {
		$tmpHostArr    = explode('.', $info['host']);
		$tmpHostArr[3] = $i;
		$host          = implode('.', $tmpHostArr);
		if (connect($info['user'], $host, $info['port'], $info['password'])) {
			error_log('[SUCCESS]' . $host);
			echo '[SUCCESS]' . $host . PHP_EOL;
		} else {
			error_log('FAILD' . $host);
			echo '[FAILD]' . $host . PHP_EOL;
		}
	}
}

/**
 * Test Connect SSH Server
 *
 * @param $user
 * @param $host
 * @param $port
 * @param $password
 * @return bool
 */
function connect($user, $host, $port, $password)
{
	if (!get_extension_funcs("ssh2")) die('PLEASE INSTALL SSH2 EXTENSION');
	if ($con = ssh2_connect($host, $port)) {
		if (@ssh2_auth_password($con, $user, $password)) {
			return TRUE;
		} else {
			return FALSE;
		}
	} else {
		return FALSE;
	}
}