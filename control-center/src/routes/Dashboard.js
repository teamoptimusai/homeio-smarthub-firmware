import { Box, Text, Wrap, WrapItem, Flex } from "@chakra-ui/react";
import { PowerPieChart } from "../components/PowerPieChart";
import { PowerUsageChart } from "../components/PowerUsageChart";
import AddDeviceBtn from "../components/AddDeviceBtn";
import DeviceBtn from "../components/DeviceBtn";

const devices = [
  {
    name: "Refrigerator",
    type: "Smart Plug Socket",
    status: "Online",
  },
  {
    name: "Kitchen Light",
    type: "Smart Light",
    status: "Online",
  },
  {
    name: "Washing Machine",
    type: "Smart Plug Socket",
    status: "Offline",
  },
  {
    name: "Microwave",
    type: "Smart Plug Socket",
    status: "Offline",
  },
  {
    name: "Air Conditioner",
    type: "Smart AC Controller",
    status: "Online",
  },
];

export default function Dashboard() {
  return (
    // Align all the items to the left
    <Box>
      <Text fontSize="5xl">Dashboard</Text>
      <Flex>
        <Box
          flex={4}
          backgroundColor="blackAlpha.300"
          borderRadius={5}
          marginTop={3}
          padding={5}
          width="100%"
        >
          <Text paddingBottom={3}>Connected Devices</Text>
          <Wrap>
            <WrapItem>
              <AddDeviceBtn />
            </WrapItem>
            {devices.map((device, index) => (
              <WrapItem key={index}>
                <DeviceBtn device={device} />
              </WrapItem>
            ))}
          </Wrap>
        </Box>
        <Box
          flex={1}
          marginLeft={3}
          backgroundColor="blackAlpha.300"
          borderRadius={5}
          marginTop={3}
          padding={5}
          width="100%"
        >
          <Text paddingBottom={3}>Monthly Power Usage</Text>
          <PowerPieChart />
        </Box>
      </Flex>
      <Box
        backgroundColor="blackAlpha.300"
        borderRadius={5}
        marginTop={3}
        padding={5}
        width="100%"
      >
        <Text paddingBottom={6}>Today's Power Usage</Text>
        <PowerUsageChart />
      </Box>
    </Box>
  );
}
