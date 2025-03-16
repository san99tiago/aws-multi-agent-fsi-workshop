install:
	cd lambda-layers && $(MAKE) install
	cd frontend && $(MAKE) install

clean:
	cd lambda-layers && $(MAKE) clean
	cd frontend && $(MAKE) clean
