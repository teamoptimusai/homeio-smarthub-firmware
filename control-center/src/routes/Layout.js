import React from "react";
import { Box, Text, Flex, Grid, Image } from "@chakra-ui/react";
import { ColorModeSwitcher } from "../ColorModeSwitcher";
import { Outlet } from "react-router-dom";

function App() {
  return (
    <Box>
      <Flex minH="100vh" p={10} flexDirection="column">
        <Flex justifyContent={"space-between"} height={10} marginBottom={6}>
          <Flex>
            <Image src="/logo.png" marginRight={3} height={50} />
            <Flex flexDirection="column" alignItems="baseline">
              <Text fontSize={"sm"}>Welcome to</Text>
              <Text fontSize="md">HomeIO Control Center </Text>
            </Flex>
          </Flex>
          <ColorModeSwitcher justifySelf="flex-end" />
        </Flex>
        <Grid overflow="auto">
          <Outlet />
        </Grid>
        <Text>Copyrights are </Text>
      </Flex>
    </Box>
  );
}

export default App;
