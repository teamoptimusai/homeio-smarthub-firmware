import {
  Button,
  Text,
  useDisclosure,
  Drawer,
  DrawerBody,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  DrawerFooter,
  Input,
} from "@chakra-ui/react";
import React from "react";

const AddDeviceBtn = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const AddbtnRef = React.useRef();

  return (
    <>
      <Button
        boxSize={150}
        shadow="xl"
        ref={AddbtnRef}
        onClick={onOpen}
        colorScheme="purple"
      >
        <Text fontSize="4xl">+</Text>
      </Button>
      <Drawer
        isOpen={isOpen}
        placement="right"
        onClose={onClose}
        finalFocusRef={AddbtnRef}
        size="md"
      >
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader>Add New Device</DrawerHeader>

          <DrawerBody>
            <Input placeholder="Type here..." />
          </DrawerBody>

          <DrawerFooter>
            <Button variant="outline" mr={3} onClick={onClose}>
              Cancel
            </Button>
            <Button colorScheme="blue">Save</Button>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </>
  );
};

export default AddDeviceBtn;
