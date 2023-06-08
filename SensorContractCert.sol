pragma solidity ^0.8.17;

contract IoTForensics {

	event deviceEvent(address indexed _from, string _message);
	event setHashEvent(address indexed _from, string _message);

	struct Certificate {
		uint256 id;
		bytes certData;
		string cert_owner;
	}
	
	struct Evidence {
		string hash;
		uint timestamp;
		string cert_owner;
	}

	mapping(uint => Evidence) evidence;
	mapping(uint256 => Certificate) registeredCertificates;
	
	//Current readings
	uint public currentID;
	
	//Contract created by
	address private contractCreator;
	
	//Constructor for Smart Contract
	constructor() {
		currentID = 1;
		contractCreator = msg.sender;
	}

	function registerCertificate(uint256 certificateId, bytes calldata certificate, string calldata cert_owner) public {
		require(msg.sender == contractCreator, "Only contract creator can register certificates");
		Certificate storage certificateRegister = registeredCertificates[certificateId];
		certificateRegister.id = certificateId;
		certificateRegister.certData = certificate;
		certificateRegister.cert_owner = cert_owner;
	}

	
	function getID() public view returns(uint) {
		return currentID;
	}
	
	function incrementID() public {
		currentID++;
	}
	
	function storeEvidence(string calldata _filehash, uint256 certificateId, bytes calldata cert, string calldata cert_owner) public {
		Certificate storage certificateStore = registeredCertificates[certificateId];
		require(keccak256(certificateStore.certData) == keccak256(cert), "Invalid certificate");

		uint hashID = getID();
		Evidence storage evidenceToStore = evidence[hashID];
			
		evidenceToStore.hash = _filehash;
		evidenceToStore.timestamp = block.timestamp;
		evidenceToStore.cert_owner = cert_owner;

		incrementID();
			
		emit setHashEvent(msg.sender, "Transaction called successfully");
	}
	
	function getLatestEvidence(uint256 certificateId, bytes calldata cert) public returns(uint, string memory, uint, string memory) {
		Certificate storage certificateRetrieve = registeredCertificates[certificateId];
		require(keccak256(certificateRetrieve.certData) == keccak256(cert), "Invalid certificate");

		Evidence storage evidenceToRead = evidence[getID()-1];
		emit deviceEvent(msg.sender, "Obtained latest evidence from the blockchain");
		return (getID()-1, evidenceToRead.hash, evidenceToRead.timestamp, evidenceToRead.cert_owner);
	}	
}
