import {
  Button,
  Box,
  Text,
  useDisclosure,
  Drawer,
  DrawerBody,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  StatGroup,
  // DrawerCloseButton,
  DrawerFooter,
  // Input,
  Badge,
} from "@chakra-ui/react";
import React from "react";
import { PowerUsageChart } from "./PowerUsageChart";

const DeviceBtn = ({ device }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const btnRef = React.useRef();

  return (
    <>
      <Button
        height={150}
        width={250}
        shadow="xl"
        onClick={onOpen}
        ref={btnRef}
      >
        <Box>
          <Text fontSize="2xl">{device.name}</Text>
          <Text>{device.type}</Text>
          {device.status === "Online" ? (
            <Badge colorScheme="green">Online</Badge>
          ) : (
            <Badge colorScheme="red">Offline</Badge>
          )}
        </Box>
      </Button>
      <Drawer
        isOpen={isOpen}
        placement="right"
        onClose={onClose}
        finalFocusRef={btnRef}
        size="lg"
      >
        <DrawerOverlay />
        <DrawerContent>
          {/* <DrawerCloseButton /> */}
          <DrawerHeader>
            <Text fontSize="3xl">{device.name}</Text>
            {device.status === "Online" ? (
              <Badge colorScheme="green">Online</Badge>
            ) : (
              <Badge colorScheme="red">Offline</Badge>
            )}
          </DrawerHeader>

          <DrawerBody>
            <StatGroup>
              <Stat
                backgroundColor="blackAlpha.300"
                borderRadius={5}
                padding={3}
                marginRight={3}
              >
                <StatLabel>Energy Usage (May)</StatLabel>
                <StatNumber>34 kWh</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  3.36%
                </StatHelpText>
              </Stat>

              <Stat
                backgroundColor="blackAlpha.300"
                borderRadius={5}
                padding={3}
                marginRight={3}
              >
                <StatLabel>Current Power Usage</StatLabel>
                <StatNumber>45 W</StatNumber>
                <StatHelpText>
                  <StatArrow type="decrease" />
                  9.05%
                </StatHelpText>
              </Stat>

              <Stat
                backgroundColor="blackAlpha.300"
                borderRadius={5}
                padding={3}
                marginRight={3}
              >
                <StatLabel>Active Time (Daily)</StatLabel>
                <StatNumber>16 h</StatNumber>
                <StatHelpText>
                  <StatArrow type="decrease" />
                  5.05%
                </StatHelpText>
              </Stat>
            </StatGroup>
            <PowerUsageChart />
          </DrawerBody>

          <DrawerFooter>
            <Button
              variant="outline"
              mr={3}
              onClick={onClose}
              colorScheme="red"
            >
              Remove
            </Button>
            <Button colorScheme="blue">Edit</Button>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </>
  );
};

export default DeviceBtn;
